# Generated by Django 3.2.5 on 2023-02-02 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0003_alter_appuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='default1.png', null=True, upload_to=''),
        ),
    ]
