from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default='default.png', upload_to='profile_pics')
    wall_image=models.ImageField(default='wood.jpg', upload_to='wall_pic')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        img=Image.open(self.image)

        output = BytesIO()

        img = img.resize((300,300), Image.ANTIALIAS)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.save(output, format='JPEG', quality=100)
        output.seek(0)

        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        print(self.image.name)
        super(Profile, self).save(*args, **kwargs)


class UserFollowing(models.Model):
    id=models.AutoField(primary_key=True)
    loggedInUser = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    toFollowUser = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
