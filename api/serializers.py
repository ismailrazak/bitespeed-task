from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import serializers

from api.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True)

    class Meta:
        model = Contact
        fields = (
            "id",
            "email",
            "phone_number",
            "linked_id",
            "linked_precedence",
            "created_at",
            "updated_at",
            "deleted_at",
        )
        read_only_fields = (
            "linked_id",
            "linked_precedence",
            "created_at",
            "updated_at",
            "deleted_at",
        )

    def validate(self, data):
        email = data.get("email")
        phone_number = data.get("phone_number")
        if not email and not phone_number:
            raise serializers.ValidationError({"error": "both fields cannot be blank."})
        # if phone_number.is_digit():
        #     raise serializers.ValidationError("Phone number must be a valid  phone number.")
        return data

    def create(self, validated_data):
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")
        contacts = Contact.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
        ).order_by("created_at")
        if contacts:
            oldest_contact = contacts[0]
            if oldest_contact.linked_precedence == "primary":

                primary_contacts = contacts.filter(linked_precedence="primary").exclude(
                    email=oldest_contact.email
                )
                if primary_contacts:
                    for contact in primary_contacts:
                        contact.linked_id = oldest_contact
                        contact.linked_precedence = "secondary"
                        contact.save()
                    return oldest_contact
            else:
                oldest_contact = oldest_contact.linked_id
            if email != "" and phone_number != "":
                new_secondary_contact = Contact.objects.create(
                    email=email,
                    phone_number=phone_number,
                    linked_id=oldest_contact,
                    linked_precedence="secondary",
                )
                return new_secondary_contact
        if email != "" and phone_number != "":
            new_primary_contact = Contact.objects.create(
                email=email, phone_number=phone_number, linked_precedence="primary"
            )
            return new_primary_contact
        return contacts.first()
