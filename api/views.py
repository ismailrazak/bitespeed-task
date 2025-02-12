from enum import unique

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Contact
from api.serializers import ContactSerializer


def _filter_duplicate_emails(primary_contact):
    emails = [primary_contact.email]
    secondary_contacts = primary_contact.secondary_contacts.all()
    for contact in secondary_contacts:
        if contact.email not in emails:
            emails.append(contact.email)
    return emails


def _filter_duplicate_phone_numbers(primary_contact):
    phone_numbers = [primary_contact.phone_number]
    secondary_contacts = primary_contact.secondary_contacts.all()
    for contact in secondary_contacts:
        if contact.phone_number not in phone_numbers:
            phone_numbers.append(contact.phone_number)
    return phone_numbers


def _response_for_contact(unique_contact):
    emails = _filter_duplicate_emails(unique_contact)
    phone_numbers = _filter_duplicate_phone_numbers(unique_contact)
    data = {
        "contact": {
            "primaryContatctId": unique_contact.id,
            "emails": emails,
            "phoneNumbers": phone_numbers,
            "secondaryContactIds": [
                contact.id for contact in unique_contact.secondary_contacts.all()
            ],
        }
    }
    return Response(data=data, status=status.HTTP_200_OK)


class IdentifyView(APIView):
    def post(self, request, pk=None):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        contact = Contact.objects.filter(
            Q(email=email) & Q(phone_number=phone_number)
        ).first()
        if contact:
            unique_contact = contact
            if unique_contact.linked_precedence == "primary":
                return _response_for_contact(unique_contact)
            else:
                primary_contact = unique_contact.linked_id
                return _response_for_contact(primary_contact)
        serializer.save()
        if serializer.data.get("linked_precedence") == "primary":
            primary_contact_id = serializer.data.get("id")
            print(primary_contact_id)
            unique_contact = Contact.objects.get(id=primary_contact_id)
            return _response_for_contact(unique_contact)
        else:
            primary_contact = serializer.data.get("linked_id")

            unique_contact = Contact.objects.get(id=primary_contact)
            return _response_for_contact(unique_contact)
