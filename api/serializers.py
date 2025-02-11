from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.db.models import Q
from api.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True,allow_null=True)
    phone_number = serializers.IntegerField(allow_null=True)
    class Meta:
        model = Contact
        fields = ( 'email', 'phone_number', 'linked_id', 'linked_precedence', 'created_at', 'updated_at', 'deleted_at', )
        read_only_fields = ( 'linked_id', 'linked_precedence', 'created_at', 'updated_at', 'deleted_at', )

    def create(self, validated_data):

            email=validated_data.get("email")
            phone_number =validated_data.get("phone_number")
            contact = Contact.objects.filter(email=email,phone_number=phone_number)
            primary_contacts = Contact.objects.filter(Q(email=email)| Q(phone_number=phone_number)).order_by("created_at")
            if contact:
                return contact
            elif primary_contacts:
                print("primary_contacts",primary_contacts)
                primary_contact=primary_contacts.first()
                for contact in primary_contacts[1:]:
                    contact.linked_id =primary_contact.id
                    contact.linked_precedence='secondary'
                    contact.save()
                if primary_contacts.count()==1:
                    print(primary_contacts)
                    secondary_contact=Contact.objects.create(linked_id = primary_contact.id,linked_precedence="secondary",**validated_data)
                    return secondary_contact
                return primary_contact
            else:
                new_primary_contact=Contact.objects.create(linked_precedence='primary',**validated_data)
                print("new_primary_contact",new_primary_contact)
                return new_primary_contact


# TODO : FIX NULL ALSO BEING ACCEPOTED
# TODO FIX PHONE NUMBER DUPLCITE IN REPSOEN
#TODO DIX PHONE NO TO STRING FIELDS