# Generated by Django 4.0.5 on 2022-07-06 18:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_comment_liked_by_comment_likes_delete_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcomment',
            old_name='announ_comment',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='announcomment',
            name='announ_likes',
        ),
        migrations.AddField(
            model_name='announcomment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='announcement_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
