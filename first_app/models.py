from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator



# Create your models here.

class Userr(models.Model):
	VALUES=(('Guest','Guest'),('Client','Client'),('Reception','Reception'),('Restaurant','Restaurant'),('Housekeeping','Housekeeping'))
	status=models.CharField(choices=VALUES,max_length=30)
	user=models.OneToOneField(User,on_delete=models.CASCADE)

class Room_Details(models.Model):
	CATEGORY=(('Economy','Economy'),('Deluxe','Deluxe'),('SuperDeluxe','SuperDeluxe'),('Suite','Suite'))
	VALUES=((1500,1500),(3000,3000),(4000,4000),(5000,5000))
	Room_Id=models.IntegerField(primary_key=True)
	Type=models.CharField(choices=CATEGORY,max_length=30)
	Price=models.IntegerField(choices=VALUES)

class Booking_Details(models.Model):

	VALUES=(('Check In','Check In'),('Check Out','Check Out'),('Checked Out','Checked Out'))

	Booking_Id=models.IntegerField(primary_key=True)
	Booking_Name=models.CharField(max_length=30)
	Check_in=models.DateField()
	Check_out=models.DateField()
	Room_Id=models.ManyToManyField(Room_Details)
	Advance=models.IntegerField(default=0)
	status=models.CharField(max_length=30,choices=VALUES,default='Check In')



class Accounts(models.Model):
	Booking_Id=models.IntegerField(default=0)
	Room_Id=models.IntegerField(default=0)
	Room_charges=models.IntegerField(default=0)
	Restaurant_charges=models.IntegerField(default=0)
	Tariff_charges=models.IntegerField(default=0)


class Restaurant(models.Model):

	VALUES=(('Vegetarian','Vegetarian'),('Non-Vegetarian','Non-Vegetarian'),('Bread','Bread'),('Soup','Soup'),('Dessert','Dessert'),('Chinese','Chinese'))
	Food_Item=models.CharField(primary_key=True,max_length=30)
	Price=models.IntegerField(default=0)
	Type=models.CharField(max_length=30,default='Vegetarian',choices=VALUES)


class Orders(models.Model):
	VALUES=(('Pending','Pending'),('Preparing','Preparing'),('Delivering','Delivering'),('Delivered','Delivered'))
	Order_Id=models.IntegerField(primary_key=True)
	Booking_Id=models.IntegerField(default=0)
	Room_Id=models.IntegerField(default=0)
	Status=models.CharField(max_length=30,default='Pending',choices=VALUES)
	Items=models.ManyToManyField(Restaurant,through='Number')
	


class Number(models.Model):
	Order=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
	Items=models.ForeignKey(Orders,on_delete=models.CASCADE)
	Quantity=models.IntegerField(default=0)	






class Bookings(models.Model):
	
	Date_is=models.DateField()
	Booking_Id=models.ManyToManyField(Booking_Details)
		

class Personal(models.Model):
	Booking_Id=models.IntegerField(default=0)
	Room_Id=models.IntegerField(default=0)
	Name=models.CharField(max_length=30,default='---')
	Email=models.CharField(max_length=30,default='abc@gmail.com',validators=[EmailValidator])
	PhoneNumber=models.CharField(max_length=12,default='00000')
	identity=models.ImageField(upload_to='identity',null=True)

class Housekeeping(models.Model):
	VALUES=(('Pending','Pending'),('Done','Done'))
	Booking_Id=models.IntegerField(default=0)
	Room_Id=models.IntegerField(default=0)
	Request=models.CharField(max_length=2000,default='type')
	Status=models.CharField(max_length=30,choices=VALUES,default='Pending')






