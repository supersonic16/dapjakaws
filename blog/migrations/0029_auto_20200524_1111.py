# Generated by Django 3.0.5 on 2020-05-24 11:11

from django.db import migrations
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20200524_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover_image',
            field=smartfields.fields.ImageField(upload_to=''),
        ),
    ]