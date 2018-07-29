# Generated by Django 2.0.2 on 2018-06-18 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_auto_20180618_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
