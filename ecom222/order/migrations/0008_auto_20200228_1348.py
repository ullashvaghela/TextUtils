# Generated by Django 2.2.10 on 2020-02-28 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20200228_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.RemoveField(
            model_name='orderstatus',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderstatus',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='orderstatus_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='order.OrderStatus'),
            preserve_default=False,
        ),
    ]
