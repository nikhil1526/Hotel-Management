# Generated by Django 2.2.6 on 2020-04-30 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0005_housekeeping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekeeping',
            name='Request',
            field=models.CharField(default='type', max_length=2000),
        ),
        migrations.AlterField(
            model_name='housekeeping',
            name='Status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=30),
        ),
    ]
