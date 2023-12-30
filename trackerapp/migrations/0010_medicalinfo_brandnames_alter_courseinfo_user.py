# Generated by Django 4.2.7 on 2023-12-14 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trackerapp', '0009_rename_start_dose_courseinfo_course_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalinfo',
            name='brandnames',
            field=models.TextField(default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='courseinfo',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
