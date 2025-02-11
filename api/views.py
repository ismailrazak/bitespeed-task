from django.db.models import Q
from django.shortcuts import render
from rest_framework.response import Response
from  rest_framework.views import APIView

from api.models import Contact
from api.serializers import ContactSerializer


class IdentifyView(APIView):
    def post(self,request,pk=None):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email=request.data.get('email')
        phone_number =request.data.get('phone_number')
        contacts=Contact.objects.filter(Q(email=email)|Q(phone_number=phone_number)).order_by('created_at')
        if contacts[0].linked_precedence=="secondary":
            primary_contact = Contact.objects.get(id=contacts[0].linked_id)
            contacts = Contact.objects.filter(Q(email=primary_contact.email)|Q(phone_number=primary_contact.phone_number)).order_by('created_at')
        emails=[]
        [emails.append(contact.email) for contact in contacts if contact.email not in emails]
        phone_numbers =[]
        [phone_numbers.append(contact.phone_number) for contact in contacts if contact.phone_number not in phone_numbers]
        secondary_contact_ids = [contact.id for contact in contacts[1:]]
        data = 	{
		"contact":{
			"primaryContactId": contacts[0].id,
			"emails": emails,
			"phoneNumbers": phone_numbers,
			"secondaryContactIds": secondary_contact_ids
		}
	}
        return Response(data)