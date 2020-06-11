from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class usersignup(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']


class userlogin(ModelForm):
	class Meta:
		model=User
		fields=['username','password']



class GuestForm(ModelForm):
	class Meta:
		model=Personal
		fields=['Booking_Id','Room_Id','Name','Email','PhoneNumber','identity']


class Housekeeping_form(ModelForm):
	Request=forms.CharField(widget=forms.Textarea)
	class Meta:
		model=Housekeeping
		fields=['Request',]		
