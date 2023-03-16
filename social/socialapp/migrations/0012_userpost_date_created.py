# Generated by Django 3.2 on 2023-02-08 12:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0011_alter_friends_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date created'),
            preserve_default=False,
        ),
    ]
