# Generated by Django 2.2.6 on 2019-12-11 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20191022_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entertainmentmodel',
            name='jumbotron',
            field=models.ImageField(default='no image', upload_to='jumbotron'),
        ),
    ]
