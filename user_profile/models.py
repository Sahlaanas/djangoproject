from django.db import models
from useraccount.models import Account

# Create your models here.
class User_Address(models.Model):
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    contact_number = models.CharField(max_length=12,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    address = models.TextField(max_length=300, default="Address")
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    order_note = models.TextField(max_length=300)


    def __str__(self):
        return self.firstname
