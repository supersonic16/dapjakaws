# Generated by Django 3.0.5 on 2020-04-12 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_post_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sub_title',
            field=models.CharField(max_length=100, null='True'),
            preserve_default='True',
        ),
    ]