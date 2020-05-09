from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image

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
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    jumbotron=models.ImageField(upload_to= 'media', default="no image")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img=Image.open(self.jumbotron.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.jumbotron.path)

class Post(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100, null="True")
    content = models.TextField()
    cover_image = models.ImageField(upload_to= 'media', default="no image", null="True")
    credit = models.CharField(max_length=100, default="no credits available", null="True")
    image = models.ImageField(default='default.png', upload_to= 'media')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name="author_id", on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img=Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})
