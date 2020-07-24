from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from dapjakaws.utils import unique_slug_generator
from django.db.models.signals import pre_save

# Create your models here.
class Subscribe(models.Model):
    subscriber_name=models.CharField(max_length=100)
    subscriber_email=models.EmailField(max_length=100)

    def get_absolute_url(self):
        return reverse('blog:subscribe')

classify_into = (
    ('none', 'None'),
    ('news', 'News'),
    ('entertainment', 'Entertainment'),
    ('sports', 'Sports'),
    ('tech', 'Tech'),
    ('travel', 'Travel')
)

class Post(models.Model):

    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True)
    cover_image = models.ImageField(upload_to= 'media', null=True , blank=True)
    credit = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    author = models.ForeignKey(User, related_name="author_id", on_delete=models.CASCADE)
    classification=models.CharField(max_length=20, choices=classify_into, default='none')



    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.cover_image:
            img=Image.open(self.cover_image)

            output = BytesIO()

            img = img.resize((800,600), Image.ANTIALIAS)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.save(output, format='JPEG', quality=50)
            output.seek(0)

            self.cover_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.cover_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Post, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.id, self.slug])

    def get_like_url(self):
        return reverse('blog:post-like', args=[self.id, self.slug])

    def get_api_like_url(self):
        return reverse('blog:post-like-api', args=[self.id, self.slug])

    def get_dislike_url(self):
        return reverse('blog:post-dislike', args=[self.id, self.slug])

    def get_api_dislike_url(self):
        return reverse('blog:post-dislike-api', args=[self.id, self.slug])

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)


class BlogComment(models.Model):
    sno = models.AutoField(primary_key = True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
# class Post_classification(models.Model):
#     id=models.AutoField(primary_key=True)
#     classification=models.CharField(max_length=20, null=True)
#     post_id=models.ForeignKey(Post, related_name="post_id", on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
