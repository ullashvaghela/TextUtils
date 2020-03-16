# Generated by Django 2.2.10 on 2020-02-26 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_number',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='zipcode',
            field=models.IntegerField(blank=True, default=2),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
