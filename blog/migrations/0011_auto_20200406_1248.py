# Generated by Django 2.2.6 on 2020-04-06 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date_posted',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='no image', null='True', upload_to='media'),
        ),
    ]
