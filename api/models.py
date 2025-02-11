from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Contact(models.Model):
    email = models.EmailField(blank=True,null=True)
    phone_number = models.IntegerField(blank=True,null=True)
    linked_id = models.IntegerField(blank=True,null=True)
    linked_precedence = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)

