# Generated by Django 5.0.1 on 2024-02-09 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_auto_20220425_1819_squashed_0005_rename_body_post_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostPermissions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code_name", models.CharField(max_length=256, unique=True)),
                ("description", models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="permissions",
            field=models.ManyToManyField(
                blank=True, related_name="permissions", to="api.postpermissions"
            ),
        ),
    ]
