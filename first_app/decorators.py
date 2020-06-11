from  first_app.models import Userr
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect

def  allowed_users(allowed=[]):
	def decorator(view_func):
		def wrapper_func(request,*args,**kwargs):
			username=request.user.username
			user=User.objects.get(username=username)
			print(user)
			userr=Userr.objects.get(user=user)
			print(userr)
			status=userr.status
			print(status)
			if status in allowed:
				return view_func(request,*args,**kwargs)
			else:
				return HttpResponse("You are not authorized to view this page")

		return wrapper_func
	return decorator			





