# Generated by Django 2.0.2 on 2018-07-25 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180725_1939'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': '通知消息', 'verbose_name_plural': '通知消息'},
        ),
    ]
