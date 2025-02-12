from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Contact(models.Model):
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    linked_id = models.ForeignKey(
        "Contact",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="secondary_contacts",
    )
    linked_precedence = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email
