# Generated by Django 2.2.6 on 2020-04-28 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_auto_20200428_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='Status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('Delivering', 'Delivering'), ('Delivered', 'Delivered')], default='Pending', max_length=30),
        ),
    ]