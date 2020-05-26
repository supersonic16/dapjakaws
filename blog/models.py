from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
class NameModel(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)

class ContactModel(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    message=models.CharField(max_length=500)

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

    def save(self):
        img=Image.open(self.cover_image)

        output = BytesIO()

        img = img.resize((800,600), Image.ANTIALIAS)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.save(output, format='JPEG', quality=90)
        output.seek(0)

        self.cover_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.cover_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Post, self).save()


    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})
