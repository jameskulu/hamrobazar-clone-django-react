from django.db import models
from Accounts.models import Account

class Product(models.Model):
  name = models.CharField(max_length = 100)
  description = models.TextField()
  price = models.FloatField()
  user = models.ForeignKey(Account,on_delete=models.CASCADE)
