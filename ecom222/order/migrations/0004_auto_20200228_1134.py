# Generated by Django 2.2.10 on 2020-02-28 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20200228_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_item',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='order_user_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
