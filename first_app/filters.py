from .models import *
import django_filters


class BookingFilter(django_filters.FilterSet):
	class Meta:
		model=Booking_Details
		fields={
		'Booking_Id':['exact', ],
		'Booking_Name':['exact', ],
		'Check_in':['exact','month', ],
		'Check_out':['exact','month', ],
		'status':['exact',],

		}



class OrderFilter(django_filters.FilterSet):
	class Meta:
		model=Orders
		fields={
		'Order_Id':['exact',],
		'Booking_Id':['exact',],
		'Room_Id':['exact',],
		'Status':['exact',],

		}		



class ItemFilter(django_filters.FilterSet):
	class Meta:
		model=Restaurant
		fields={
		'Food_Item':['exact','contains',],
		'Price':['exact','gte','lte',],
		'Type':['exact',],
		}



class HousekeepingFilter(django_filters.FilterSet):
	class Meta:
		model=Housekeeping
		fields={
		'Booking_Id':['exact',],
		'Room_Id':['exact',],
		'Status':['exact',],
		}		

