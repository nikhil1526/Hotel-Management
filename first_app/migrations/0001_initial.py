# Generated by Django 2.2.6 on 2020-04-27 22:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Booking_Id', models.IntegerField(default=0)),
                ('Room_Id', models.IntegerField(default=0)),
                ('Room_charges', models.IntegerField(default=0)),
                ('Restaurant_charges', models.IntegerField(default=0)),
                ('Tariff_charges', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Booking_Details',
            fields=[
                ('Booking_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Booking_Name', models.CharField(max_length=30)),
                ('Check_in', models.DateField()),
                ('Check_out', models.DateField()),
                ('Advance', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Check In', 'Check In'), ('Check Out', 'Check Out'), ('Checked Out', 'Checked Out')], default='Check In', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Booking_Id', models.IntegerField(default=0)),
                ('Room_Id', models.IntegerField(default=0)),
                ('Name', models.CharField(max_length=30)),
                ('Email', models.CharField(max_length=30, validators=[django.core.validators.EmailValidator])),
                ('PhoneNumber', models.CharField(max_length=12)),
                ('identity', models.ImageField(null=True, upload_to='identity')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('Food_Item', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Price', models.IntegerField(default=0)),
                ('Type', models.CharField(choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Bread', 'Bread'), ('Soup', 'Soup'), ('Dessert', 'Dessert'), ('Chinese', 'Chinese')], default='Vegetarian', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Room_Details',
            fields=[
                ('Room_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Type', models.CharField(choices=[('Economy', 'Economy'), ('Deluxe', 'Deluxe'), ('SuperDeluxe', 'SuperDeluxe'), ('Suite', 'Suite')], max_length=30)),
                ('Price', models.IntegerField(choices=[(1500, 1500), (3000, 3000), (4000, 4000), (5000, 5000)])),
            ],
        ),
        migrations.CreateModel(
            name='Userr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Guest', 'Guest'), ('Client', 'Client'), ('Reception', 'Reception'), ('Restaurant', 'Restaurant'), ('Housekeeping', 'Housekeeping')], max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_is', models.DateField()),
                ('Booking_Id', models.ManyToManyField(to='first_app.Booking_Details')),
            ],
        ),
        migrations.AddField(
            model_name='booking_details',
            name='Room_Id',
            field=models.ManyToManyField(to='first_app.Room_Details'),
        ),
    ]
