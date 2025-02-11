from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.db.models import Q
from api.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True)
    class Meta:
        model = Contact
        fields = ( 'email', 'phone_number', 'linked_id', 'linked_precedence', 'created_at', 'updated_at', 'deleted_at', )
        read_only_fields = ( 'linked_id', 'linked_precedence', 'created_at', 'updated_at', 'deleted_at', )
    def validate(self, data):
        email =data.get("email")
        phone_number = data.get("phone_number")
        if not email and not  phone_number:
            raise serializers.ValidationError({"error":'both fields cannot be blank.'})
        return data
    def create(self, validated_data):

            email=validated_data.get("email")
            phone_number =validated_data.get("phone_number")
            contact = Contact.objects.filter(email=email,phone_number=phone_number)
            primary_contacts = Contact.objects.filter(Q(email=email)| Q(phone_number=phone_number)).order_by("created_at")
            if contact:
                return contact
            elif primary_contacts:
                primary_contact=primary_contacts.first()
                for contact in primary_contacts[1:]:
                    contact.linked_id =primary_contact.id
                    contact.linked_precedence='secondary'
                    contact.save()
                if primary_contacts.filter(linked_precedence='primary').count()==1:
                    if email=="" or phone_number=="":
                        return primary_contact
                    secondary_contact=Contact.objects.create(linked_id = primary_contact.id,linked_precedence="secondary",**validated_data)
                    return secondary_contact
                return primary_contact
            else:
                new_primary_contact=Contact.objects.create(linked_precedence='primary',**validated_data)
                print("new_primary_contact",new_primary_contact)
                return new_primary_contact


