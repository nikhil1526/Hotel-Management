# Generated by Django 2.2.6 on 2020-04-29 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0004_auto_20200429_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Housekeeping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Booking_Id', models.IntegerField(default=0)),
                ('Room_Id', models.IntegerField(default=0)),
                ('Request', models.CharField(max_length=2000)),
                ('Status', models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done')], max_length=30)),
            ],
        ),
    ]
