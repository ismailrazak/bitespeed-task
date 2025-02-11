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
        emails = [contact.email for contact in contacts]
        phoneNumbers = [contact.phone_number for contact in contacts]
        secondaryContactIds = [contact.id for contact in contacts[1:]]
        data = 	{
		"contact":{
			"primaryContatctId": contacts[0].id,
			"emails": emails,
			"phoneNumbers": phoneNumbers,
			"secondaryContactIds": secondaryContactIds
		}
	}
        return Response(data)