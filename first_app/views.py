from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import usersignup,userlogin,GuestForm,Housekeeping_form
from first_app.models import Bookings,Room_Details,Booking_Details,Userr,Restaurant,Orders,Number,Accounts,Personal,Housekeeping
from datetime import datetime,date,timedelta

from .filters import BookingFilter,OrderFilter,ItemFilter,HousekeepingFilter
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from first_app.decorators import allowed_users

# if (request.method=='POST'):
	# 	room=int(u[0:3])
	# 	booking_id=int(u[4:])
	# 	orders=Orders.objects.all()
	# 	order_id=0
	# 	if(len(orders)>0):
	# 		order_id=orders[len(orders)-1].order_id
	# 	order_id=order_id+1	
	# 	new_order=Orders.objects.create(Order_Id=order_id,Booking_Id=booking_id,Room_Id=room)




	# 	titles=request.POST.getlist('titles')
	# 	quantity=request.POST.getlist('quantity')
	# 	combined=zip(titles,quantity)
	# 	for i,j in combined:
	# 		item_name=Restaurant.objects.get(Food_Item=i)
	# 		j=int(j)
	# 		new_order.Items.add(item_name,through_defaults={'Quantity':j})


def all_unexpired_sessions_for_user(user):
	user_sessions = []
	all_sessions  = Session.objects.filter(expire_date__gte=datetime.now())
	for session in all_sessions:
		session_data = session.get_decoded()
		if user.pk == session_data.get('_auth_user_id'):
			user_sessions.append(session)
	return user_sessions

def delete_all_unexpired_sessions_for_user(user, session_to_omit=None):
	for session in all_unexpired_sessions_for_user(user):
		if session is not session_to_omit:
			session.delete()

@login_required(login_url='/login/')
@allowed_users(allowed=['Guest'])
def guest_dashboard(request):

	username=request.user.username
	username=str(username)
	room_id=int(username[0:3])
	booking_id=int(username[4:])
	request_is=Housekeeping.objects.filter(Booking_Id=booking_id,Room_Id=room_id)
	orders=Orders.objects.filter(Booking_Id=booking_id,Room_Id=room_id)
	context={'orders':orders,'request_is':request_is}

	return render(request,'first_app/guest_dashboard.html',context)

@login_required(login_url='/login/')
@allowed_users(allowed=['Guest'])
def housekeeping_request(request):
	
	if request.method=='POST':
		username=request.user.username
		booking_id=int(username[4:])
		room_id=int(username[0:3])
		form=Housekeeping_form(request.POST)
		if form.is_valid():
			request_is=form.cleaned_data['Request']
			new_request=Housekeeping.objects.create(Booking_Id=booking_id,Room_Id=room_id,Request=request_is,Status='Pending')
			messages.success(request,'Successfully sent')

	form=Housekeeping_form()		
			
	context={'form':form}
	return render(request,'first_app/Housekeeping_request.html',context)

@login_required(login_url='/login/')
@allowed_users(allowed=['Housekeeping'])
def housekeeping(request):
	

	request_is=Housekeeping.objects.all()
	housekeeping_filter=HousekeepingFilter()
	if 'search' in request.GET:
		housekeeping_filter=HousekeepingFilter(request.GET,queryset=request_is)
		request_is=housekeeping_filter.qs
	context={'filter':housekeeping_filter,'requests':request_is}
	return render(request,'first_app/Housekeeping.html',context)


@login_required(login_url='/login/')
@allowed_users(allowed=['Housekeeping'])
def change_housekeeping(request,pk):
	request_is=Housekeeping.objects.get(id=pk)
	if(request_is.Status=='Pending'):
		request_is.Status='Done'
		request_is.save()
	else:
		request_is.Status='Pending'
		request_is.save()

	return redirect(housekeeping)				
















@login_required(login_url='/login/')
@allowed_users(allowed=['Reception'])
def extract_details(request,pk):
	detailsform=GuestForm()
	pk=int(pk)
	bookings=Booking_Details.objects.get(Booking_Id=pk)
	rooms=bookings.Room_Id
	advance=bookings.Advance

	if request.method=='POST':
		booking_id=request.POST.getlist('Booking_Id')
		room_id=request.POST.getlist('Room_Id')
		name=request.POST.getlist('Name')
		phone_number=request.POST.getlist('PhoneNumber')
		email=request.POST.getlist('Email')
		identities=request.FILES.getlist('identity')
		for i in range(0,len(booking_id)):
			Personal.objects.create(Booking_Id=booking_id[i],Room_Id=room_id[i],Name=name[i],PhoneNumber=phone_number[i],Email=email[i],identity=identities[i])


	details=Personal.objects.filter(Booking_Id=pk)
	accounts=Accounts.objects.filter(Booking_Id=pk)
	if(len(accounts)==0):
		for i in rooms.all():
			accounts=Accounts.objects.create(Booking_Id=pk,Room_Id=i.Room_Id)


	overall=0
	accounts=Accounts.objects.filter(Booking_Id=pk)
	total=[]
	for i in rooms.all():
		a=Accounts.objects.get(Booking_Id=pk,Room_Id=i.Room_Id)
		total_is=a.Room_charges+a.Restaurant_charges+a.Tariff_charges
		total.append(total_is)

	for j in total:
		overall=overall+j

	pending=overall-advance	

			




	accounts=zip(accounts,total)			



		
		
					


		

	context={'rooms':rooms,'detailsform':detailsform,'pk':pk,'accounts':accounts,'details':details,'pending':pending,'advance':advance,'overall':overall}	
	return render(request,'first_app/guest_details.html',context)		


@login_required(login_url='/login/')
@allowed_users(allowed=['Restaurant'])
def add_item(request):
	title=request.POST.get('title')
	price=request.POST.get('price')
	type_is=request.POST.get('type')
	if(Restaurant.objects.filter(Food_Item=title).exists()):
		return redirect('restaurant_page')
	else:
		new_item=Restaurant.objects.create(Food_Item=title,Price=price,Type=type_is)
		return redirect('restaurant_page')	





@login_required(login_url='/login/')
@allowed_users(allowed=['Restaurant'])
def remove_item(request,item):
	item=str(item)
	Food=Restaurant.objects.get(Food_Item=item)
	Food.delete()
	return redirect('restaurant_page')	




@login_required(login_url='/login/')
@allowed_users(allowed=['Restaurant'])
def change_item(request,item):

	price=int(request.POST.get('price'))
	
	item=str(item)
	Food=Restaurant.objects.get(Food_Item=item)
	Food.Price=price
	Food.save()
	return redirect('restaurant_page')







@login_required(login_url='/stay/login/')
@allowed_users(allowed=['Guest'])
def restaurant(request):
	global u
	if (request.method=='POST'):
		room=int(u[0:3])
		booking_id=int(u[4:])
		orders=Orders.objects.all()
		order_id=0
		if(len(orders)>0):
			order_id=orders[len(orders)-1].Order_Id
		order_id=order_id+1	
		new_order=Orders.objects.create(Order_Id=order_id,Booking_Id=booking_id,Room_Id=room)




		titles=request.POST.getlist('titles')
		quantity=request.POST.getlist('quantity')
		combined=zip(titles,quantity)
		for i,j in combined:
			item_name=Restaurant.objects.get(Food_Item=i)
			j=int(j)
			new_order.Items.add(item_name,through_defaults={'Quantity':j})

		messages.success(request,'Successfully Placed')	

	veg=Restaurant.objects.filter(Type='Vegetarian')
	non=Restaurant.objects.filter(Type='Non-Vegetarian')
	bread=Restaurant.objects.filter(Type='Bread')
	chinese=Restaurant.objects.filter(Type='Chinese')
	soup=Restaurant.objects.filter(Type='Soup')
	dessert=Restaurant.objects.filter(Type='Dessert')
	context={'veg':veg,'non':non,'bread':bread,'chinese':chinese,'soup':soup,'dessert':dessert}
	return render(request,'first_app/restaurant.html',context)

@login_required(login_url='/login/')
@allowed_users(allowed=['Restaurant'])
def restaurant_page(request):

	count=[0,0,0,0]
	orders=Orders.objects.all()
	items=Restaurant.objects.all()
	orderfilter=OrderFilter()
	itemfilter=ItemFilter()
	if('order' in request.GET):
		orderfilter=OrderFilter(request.GET,queryset=orders)
		orders=orderfilter.qs
	if('item' in request.GET):
		itemfilter=ItemFilter(request.GET,queryset=items)
		items=itemfilter.qs	

	for i in orders:
		count[0]=Orders.objects.filter(Status='Pending').count()
		count[1]=Orders.objects.filter(Status='Preparing').count()
		count[2]=Orders.objects.filter(Status='Delivering').count()
		count[3]=Orders.objects.filter(Status='Delivered').count()
	quantity=Number.objects.all()
	context={'items':items,'itemfilter':itemfilter,'orderfilter':orderfilter,'orders':orders,'quantity':quantity,'count_pe':count[0],'count_pr':count[1],'count_de':count[2],'count_dd':count[3]}

	return render(request,'first_app/restaurant_page.html',context)

@login_required(login_url='/login/')
@allowed_users(allowed=['Restaurant'])
def change_status(request,id):
	if request.method=='POST':
		order=Orders.objects.get(Order_Id=id)
		items=Number.objects.filter(Items=order)
		total=0

		status=request.POST.get('status')
		account_details=Accounts.objects.get(Booking_Id=order.Booking_Id,Room_Id=order.Room_Id)
		if(status=='Delivered'):
			
			for i in items:
				total=total+i.Order.Price*i.Quantity
		account_details.Restaurant_charges=account_details.Restaurant_charges+total
		account_details.save()
				
		order.Status=status
		order.save()
		return redirect('restaurant_page')




def abc(request):
	return render(request,'first_app/index.html')


def stay(request):
	return render(request,'first_app/stayin.html')	

@login_required(login_url='/login/')
@allowed_users(allowed=['Reception'])
def check(request,pk):
	booking_details=Booking_Details.objects.get(Booking_Id=pk)
	if(booking_details.status=='Check In'):
		return checkin(request,pk)
	elif(booking_details.status=='Check Out'):
		return checkout(request,pk)	
	else:
		return redirect('details')	








@login_required(login_url='/login/')
@allowed_users(allowed=['Reception'])
def checkout(request,pk):
	booking_details=Booking_Details.objects.get(Booking_Id=pk)
	name=booking_details.Booking_Name
	rooms=booking_details.Room_Id.all()
	checkin=str(booking_details.Check_in)
	for i in rooms:
		room_id=str(i.Room_Id)
		username=room_id+'@'+pk
		user=User.objects.get(username=username)
		delete_all_unexpired_sessions_for_user(user=user)
		user.is_active= False
		user.save()
		user.delete()

	booking_details.status='Checked Out'	
	booking_details.save()	

	return redirect('details')





@login_required(login_url='/login/')
@allowed_users(allowed=['Reception'])
def checkin(request,pk):
	booking_details=Booking_Details.objects.get(Booking_Id=pk)
	name=booking_details.Booking_Name
	rooms=booking_details.Room_Id.all()
	checkin=(booking_details.Check_in)
	check_out=booking_details.Check_out
	delta=check_out-checkin
	for i in rooms:
		room_id=str(i.Room_Id)
		price=int(i.Price)
		username=room_id+'@'+pk
		password=room_id+'@'+name
		room_id=int(room_id)
		
		user=User.objects.create_user(username=username,password=password)
		user.save()
		userr=Userr.objects.create(user=user,status='Guest')


	if(Accounts.objects.filter(Booking_Id=pk).exists()):
		for i in rooms:
			room_id=int(i.Room_Id)
			account_details=Accounts.objects.get(Booking_Id=pk,Room_Id=room_id)
			account_details.Room_charges=price*(delta.days)
			account_details.save()

	else:
		for i in rooms.all():
			room_id=int(i.Room_Id)				
			account_details=Accounts.objects.create(Booking_Id=pk,Room_Id=room_id,Room_charges=price*(delta.days))



	booking_details.status='Check Out'	
	booking_details.save()





		








	return redirect('details')



@login_required(login_url='/login/')
@allowed_users(allowed=['Client'])
def dashboard(request):
	global u
	today_date=date.today()
	current_bookings=Booking_Details.objects.filter(Booking_Name=u,Check_in__gte=today_date)
	last_bookings=Booking_Details.objects.filter(Booking_Name=u,Check_in__lt=today_date)

	context={'current':current_bookings,'last':last_bookings}

	return render(request,'first_app/dashboard.html',context)

@login_required(login_url='/login/')
@allowed_users(allowed=['Reception','Client'])
def home(request):
	global u
	user_is=User.objects.get(username=u)
	user=Userr.objects.get(user=user_is)
	if(user.status=='Reception'):
		return redirect('reception')
	if(user.status=='Client'):
		return redirect('dashboard')









@login_required(login_url='/login/')
@allowed_users(allowed=['Reception'])
def details(request):
	today_date=date.today()
	bookings=Bookings.objects.filter(Date_is__gte=today_date)
	detailed=Booking_Details.objects.none()
	if(len(bookings)>0):
		for i in bookings:
			temp=i.Booking_Id.all()
			detailed=(detailed|temp)

		detailed=detailed.distinct()
		
			


	last_bookings=Bookings.objects.filter(Date_is__lt=today_date)
	
	last_detailed=Booking_Details.objects.none()
	if(len(last_bookings)>0):
		for i in last_bookings:
			temp=i.Booking_Id.filter(Check_out__lt=today_date)
			last_detailed=last_detailed|temp
			

		last_detailed=last_detailed.distinct()
		
	current_filter=BookingFilter()
	past_filter=BookingFilter()

	if 'current' in request.GET:
		current_filter=BookingFilter(request.GET,queryset=detailed)
		detailed=current_filter.qs		

	if 'past' in request.GET:
		past_filter=BookingFilter(request.GET,queryset=last_detailed)
		last_detailed=past_filter.qs	


		
		
		

			

	




	context={'details':detailed,'last':last_detailed,'filter_current':current_filter,'filter_past':past_filter}		

					







	return render(request,'first_app/details.html',context)




def sign(request):
	form=usersignup()
	if(request.method=='POST'):
		u=str(request.POST.get('username'))
		value=int(0)
		for i in range(0,len(u)):
			if (ord(u[i])>=97 and ord(u[i])<=122) or (ord(u[i])>=65 and ord(u[i])<=90):
				value=value+1
		if(value==0):
			messages.error(request,'Unsuccessful')
			messages.error(request,'Username must have at least one alphabet')
		else:	
						
			form=usersignup(request.POST)

			if form.is_valid():
				
				form.save()
				user_is=User.objects.get(username=u)
				userr=Userr.objects.create(user=user_is,status='Client')
				messages.success(request,'Successfully signed up')

	context={'form':form}

	return render(request,'first_app/sign.html',context)	

def log_in(request):
	form=userlogin()
	context={'form':form}
	if(request.method=='POST'):
		username=request.POST.get('username')
		password=request.POST.get('Password')
		

		user=authenticate(username=username, password=password)
		global u
		u=username

		if user:
			

			if user.is_active:
				login(request,user)
				position=Userr.objects.get(user=user)

				if(position.status=='Reception'):
					return redirect('reception')
				elif(position.status=='Client'):	
					return redirect('dashboard')
				elif(position.status=='Restaurant'):
					return redirect('restaurant_page')
				elif(position.status=='Housekeeping'):
					return redirect('housekeeping')		
				else:
					messages.error(request,"Invalid Login Details")
					return render(request,'first_app/log.html',context)	

		else:
			messages.error(request,"Invalid Login Details")
			return render(request,'first_app/log.html',context)

	else:
		return render(request,'first_app/log.html',context)

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))	



def stay_log_in(request):
	if(request.method=='POST'):
		username=request.POST.get('Username')
		password=request.POST.get('Password')
		

		user=authenticate(username=username, password=password)
		global u
		u=username

		if user:
			

			if user.is_active:
				login(request,user)
				position=Userr.objects.get(user=user)

				if(position.status=='Guest'):
					return redirect('guest_dashboard')
				else:
					messages.error(request,"Invalid Login Details")
					return render(request,'first_app/stayin.html')	

		else:
			messages.error(request,"Invalid Login Details")
			return render(request,'first_app/stayin.html')

	else:
		return render(request,'first_app/stayin.html')

def stay_user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('stay_login'))		

@login_required(login_url='/login/')
@allowed_users(allowed=['Reception','Client'])
def book(request):
	return redirect('checking')

@login_required(login_url='/login/')
@allowed_users(allowed=['Client','Reception'])
def book_rooms(request):
	if request.method=='POST':
		global u
		today_date=date.today()
		todays=datetime.now()
		context={'count_e':10,'count_d':8,'count_s':6,'count_su':4 }
		checkin=request.POST.get('checki')
		checkout=request.POST.get('checko')
		number=int(request.POST.get('number'))
		types=request.POST.get('type')
		dateis=str(checkin)
		dateout=str(checkout)
		dateis=datetime.strptime(dateis,"%m/%d/%Y")
		dateout=datetime.strptime(dateout,"%m/%d/%Y")
		datein=dateis
		if(datein>=dateout or datein<todays):

			messages.error(request,"Please enter valid dates")
			context={'count_e':10,'count_d':8,'count_s':6,'count_su':4 }
			return render(request,'first_app/Booking.html',context)
		rooms_temp=Room_Details.objects.filter(Type=types)
		while (1):
			try:
				a=Bookings.objects.get(Date_is=dateis)

			except:
				a=None
				dateis=dateis+timedelta(days=1)
				if(dateis>dateout):
					break

				continue
			room=a.Booking_Id.all()
			for i in room:
				rooms=i.Room_Id.filter(Type=types)
				rooms_temp=[value for value in rooms_temp if value not in rooms]
				
			
			
			
			dateis=dateis+timedelta(days=1)
			if(dateis>dateout):
				break

		if len(rooms_temp)>=number:
			bookingid=0
			bookingids=Booking_Details.objects.all()
			if len(bookingids)>0:
				bookingid=bookingids[len(bookingids)-1].Booking_Id
			bookingid=bookingid+1

			new_booking=Booking_Details.objects.create(Booking_Id=bookingid,Booking_Name=u,Check_in=datein,Check_out=dateout)
			for i in range(number):
				new_booking.Room_Id.add(rooms_temp[i])

			while(1):
				try:
					new_bookings=Bookings.objects.get(Date_is=datein)
				except:
					new_bookings=Bookings.objects.create(Date_is=datein)

				new_bookings.Booking_Id.add(bookingid)
				datein=datein+timedelta(days=1)
				if(datein>dateout):
					break
		else:
			messages.error(request,"Sorry,Not enough rooms available")
			context={'count_e':10,'count_d':8,'count_s':6,'count_su':4 }
			return render(request,'first_app/Booking.html',context)		

					



				

		messages.success(request,"Successfully Booked")
		return render(request,'first_app/Booking.html',context)		
				




@login_required(login_url='/login/')
@allowed_users(allowed=['Client','Reception'])
def checking(request):
	count=[10,8,6,4]

	if request.method=='POST':
		today_date=date.today()
		todays=datetime.now()
		checkin=request.POST.get('checkin')
		checkout=request.POST.get('checkout')
		dateis=str(checkin)
		dateout=str(checkout)
		dateis=datetime.strptime(dateis,"%m/%d/%Y")
		dateout=datetime.strptime(dateout,"%m/%d/%Y")
		
		if(dateis>=dateout or dateis<todays):

			messages.error(request,"Please enter valid dates")
			context={'count_e':10,'count_d':8,'count_s':6,'count_su':4 }
			return render(request,'first_app/Booking.html',context)
		rooms_temp=Room_Details.objects.all()
		while (1):
			try:
				a=Bookings.objects.get(Date_is=dateis)

			except:
				a=None
				dateis=dateis+timedelta(days=1)
				if(dateis>dateout):
					break

				continue
			room=a.Booking_Id.all()
			for i in room:
				rooms=i.Room_Id.all()
				rooms_temp=[value for value in rooms_temp if value not in rooms]
				
			
			
			
			dateis=dateis+timedelta(days=1)
			if(dateis>dateout):
				break

		count=[0,0,0,0]
		# print(rooms_temp)
		for i in rooms_temp:
			if (i.Type=='Economy'):
				count[0]=count[0]+1
			elif (i.Type=='Deluxe'):
				count[1]=count[1]+1
			elif (i.Type=='SuperDeluxe'):
				count[2]=count[2]+1
			else:
				count[3]=count[3]+1

	context={'count_e':count[0],'count_d':count[1],'count_s':count[2],'count_su':count[3] }

	return render(request,'first_app/Booking.html',context)		


@login_required(login_url='/login/')
@allowed_users(allowed=['Reception'])
def reception(request):
			
	today_date=date.today()
	month=int(today_date.strftime("%m"))
	year=int(today_date.strftime("%Y"))
	month_date=datetime(year,month,1)
	month_date=month_date.date()
	months=[]
	number_of_rooms_month=[]
	if request.method=='POST':
		date_is=str(request.POST.get('date'))
		today_date=datetime.strptime(date_is,"%m/%d/%Y")
		today_date=today_date.date()



	dates=[]
	for i in range(0,7):
		dates.append(today_date-timedelta(days=i+1))

	rooms=[]	
	number_of_rooms=[]
	rooms_temp=[]
	types=['Economy','Deluxe','SuperDeluxe','Suite']

	for i in range(0,7):
		number_of_rooms.append([0,0,0,0])
		try:
			a=Bookings.objects.get(Date_is=dates[i])

		except:
			a=None
			
			

			continue
		room=a.Booking_Id.all()
		for j in room:
			for k in range(0,4):
				number_of_rooms[i][k]=number_of_rooms[i][k]+j.Room_Id.filter(Type=types[k]).count()


	count=[1,2,3,4,5,6,7]
	total=0
	revenue=0

	cost=[1500,3000,4000,5000]
	
	for i in range(0,7):
		for k in range(0,4):
			total=total+number_of_rooms[i][k]
			revenue=revenue+number_of_rooms[i][k]*cost[k]

		number_of_rooms[i].append(total)
		number_of_rooms[i].append(revenue)
		total=0	
		revenue=0

	month_date=month_date-timedelta(days=1)
	print(month_date)
	months.append(month_date.strftime("%B"))
	for i in range(0,5):
		number_of_rooms_month.append([0,0,0,0])

		while(1):
			try:
				a=Bookings.objects.get(Date_is=month_date)

			except:
				a=None
				if int(month_date.strftime("%d"))== 1:
					month_date=month_date-timedelta(days=1)
					months.append(month_date.strftime("%B"))
					break
				month_date=month_date-timedelta(days=1)
			
			

				continue
			room=a.Booking_Id.all()
			for j in room:
				for k in range(0,4):
					number_of_rooms_month[i][k]=(number_of_rooms_month[i][k]+j.Room_Id.filter(Type=types[k]).count())
			if int(month_date.strftime("%d"))== 1:
				month_date=month_date-timedelta(days=1)
				months.append(month_date.strftime("%B"))
				break
			month_date=month_date-timedelta(days=1)


	total=0
	
	for i in range(0,5):
		for k in range(0,4):
			number_of_rooms_month[i][k]=number_of_rooms_month[i][k]*cost[k]
			total=total+number_of_rooms_month[i][k]
			

		number_of_rooms_month[i].append(total)
		
		total=0	
					

			

			
					








	month_zipped=zip(months,number_of_rooms_month)
	zipped=zip(dates,number_of_rooms,count)


	
	context={'number':zipped,'dates':dates,'rooms':number_of_rooms,'months':months,'month':month_zipped,'month_rooms':number_of_rooms_month}



	return render(request,'first_app/reception.html',context)	





			





			


			