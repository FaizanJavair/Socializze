# Generated by Django 3.2 on 2023-02-05 13:59

from django.db import migrations, models
import socialapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0008_alter_userpost_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='post_image',
            field=models.FileField(blank=True, null=True, upload_to=socialapp.models.get_file_path),
        ),
    ]
