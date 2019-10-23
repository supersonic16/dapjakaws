from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class NameModel(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)

class ContactModel(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    message=models.CharField(max_length=500)

class EntertainmentModel(models.Model):
    id=models.AutoField(primary_key=True)
    heading=models.CharField(max_length=100)
    content=models.TextField(max_length=500)
    author=models.TextField(max_length=100,default="Sanchit Gupta")
    jumbotron=models.ImageField(upload_to= 'static/', default="no image")
    source=models.URLField(max_length=200,default="Not available")
