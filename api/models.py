from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)

class Contact(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="contacts")
    email = models.EmailField(blank=True,null=True)
    phone_number = models.IntegerField(blank=True,null=True)
    linked_id = models.IntegerField(blank=True,null=True)
    linked_precedence = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)

    # def save(self,*args,**kwargs)
    #     primary_contact = Contact.objects.get(linked_precedence="primary")
    #     if primary_contact:
    #         self.linked_precedence="secondary"
    #         self.linked_id=primary_contact.id
    #     else:
    #         self.linked_precedence="primary"
    #     super().save(*args, **kwargs)
    #