# Generated by Django 4.1.3 on 2022-12-27 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_post_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
        migrations.AddField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
