from django.db import models
from django.db.models import CharField, ForeignKey
from django.contrib.auth.models import User

# Create your models here.
class Resume(models.Model):
    author = ForeignKey(User, on_delete=models.CASCADE)
    description = CharField(max_length=1024)
