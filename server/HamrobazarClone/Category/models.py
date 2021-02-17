from django.db import models

class Category(models.Model):
  name = models.CharField(max_length = 100)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)