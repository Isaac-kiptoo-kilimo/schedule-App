# Generated by Django 4.0.5 on 2022-07-06 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_comment_likes_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='likes_by',
            new_name='liked_by',
        ),
    ]
