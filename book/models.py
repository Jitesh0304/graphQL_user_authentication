from django.db import models
from account.models import User




class Book(models.Model):
    name = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
