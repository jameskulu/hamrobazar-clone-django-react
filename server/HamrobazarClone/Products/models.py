from django.db import models
from Accounts.models import Account

class Product(models.Model):
  name = models.CharField(max_length = 100)
  description = models.TextField()
  price = models.FloatField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(Account,on_delete=models.CASCADE)
