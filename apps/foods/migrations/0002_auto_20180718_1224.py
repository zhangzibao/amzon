# Generated by Django 2.0.2 on 2018-07-18 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ratings',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uid', to=settings.AUTH_USER_MODEL, verbose_name='评论者id'),
        ),
        migrations.AddField(
            model_name='kinds',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='所属商家', to=settings.AUTH_USER_MODEL, verbose_name='商家id'),
        ),
        migrations.AddField(
            model_name='foods',
            name='kinds',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foods', to='foods.Kinds', verbose_name='所属分类'),
        ),
    ]
