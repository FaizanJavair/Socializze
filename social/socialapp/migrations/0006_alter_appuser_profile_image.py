# Generated by Django 3.2.5 on 2023-02-02 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0005_alter_appuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='profile_img'),
        ),
    ]
