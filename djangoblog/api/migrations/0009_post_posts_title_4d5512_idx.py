# Generated by Django 5.0.6 on 2024-08-19 19:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_post_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['title', 'views'], name='posts_title_4d5512_idx'),
        ),
    ]
