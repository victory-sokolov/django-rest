# Generated by Django 5.0.6 on 2024-08-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_tags_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(verbose_name='created_at'),
        ),
    ]
