# Generated by Django 4.2.7 on 2023-12-10 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trackerapp', '0004_dosesinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dosesinfo',
            old_name='eatmodel',
            new_name='course',
        ),
    ]
