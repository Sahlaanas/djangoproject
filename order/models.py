from django.db import models
from useraccount.models import Account

# Create your models here.
class Wallet(models.Model):
      user = models.ForeignKey(Account, on_delete=models.CASCADE)
      wallet = models.PositiveIntegerField(null=True)
      