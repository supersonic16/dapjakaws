# Generated by Django 3.0.5 on 2020-05-25 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20200524_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='classification',
        ),
        migrations.AlterField(
            model_name='post',
            name='credit',
            field=models.CharField(max_length=100, null='True'),
        ),
        migrations.CreateModel(
            name='Post_classification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('classification', models.CharField(max_length=20, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_id', to='blog.Post')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_id', to='blog.Post')),
            ],
        ),
    ]