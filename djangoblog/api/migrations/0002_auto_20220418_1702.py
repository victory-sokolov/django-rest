# Generated by Django 3.2.9 on 2022-04-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ("created_at",)},
        ),
        migrations.AddField(
            model_name="tags",
            name="slug",
            field=models.SlugField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="tag",
            field=models.ManyToManyField(
                blank=True,
                related_name="posts",
                to="api.Tags",
            ),
        ),
        migrations.AlterField(
            model_name="tags",
            name="tag",
            field=models.CharField(max_length=20),
        ),
    ]
