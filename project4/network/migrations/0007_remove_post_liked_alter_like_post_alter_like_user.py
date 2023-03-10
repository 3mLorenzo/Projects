# Generated by Django 4.1.3 on 2022-12-27 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_remove_post_like_post_liked_alter_like_post_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='liked',
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_like', to='network.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
