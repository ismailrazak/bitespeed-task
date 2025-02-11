from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.db.models import Q
from api.models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('customer', 'email', 'phone_number', 'linked_id', 'linked_precedence', 'created_at', 'updated_at', 'deleted_at', )


    def create(self, validated_data):

            email=validated_data.get("email")
            phone_number =validated_data.get("phone_number")
            contact = Contact.objects.filter(email=email,phone_number=phone_number)
            if contact:
                return contact
            primary_contact = Contact.objects.filter(Q(email=email),Q(phone_number=phone_number),linked_precedence="primary")
            if primary_contact:
                secondary_contact=Contact.objects.create(linked_id = primary_contact.id,linked_precedence="secondary",**validated_data)
                return secondary_contact
            new_primary_contact=Contact.objects.create(linked_precedence='primary',**validated_data)
            return new_primary_contact


