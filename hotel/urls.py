"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from first_app import views
from django.conf.urls import include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.abc,name='abc'),
    path('signup/',views.sign,name='sign'),
    path('login/',views.log_in,name='login'),
    path('booking/',views.book,name='book'),
    path('checking/',views.checking,name='checking'),
    path('book/',views.book_rooms,name='book_rooms'),
    path('reception/',views.reception,name='reception'),
    path('reception/details/',views.details,name='details'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('home/',views.home,name='home'),
    path('logout/',views.user_logout,name='logout'),
    path('check/<str:pk>/',views.check,name='check'),
    path('stay/',views.stay,name='stay'),
    path('stay/login/',views.stay_log_in,name='stay_login'),
    path('restaurant/',views.restaurant,name='restaurant'),
    path('staylogout/',views.stay_user_logout,name='staylogout'),
    path('restaurant_page/',views.restaurant_page,name='restaurant_page'),
    path('change_status/<str:id>/',views.change_status,name='change_status'),
    path('add/',views.add_item,name='add'),
    path('remove/<str:item>/',views.remove_item,name='remove'),
    path('change/<str:item>/',views.change_item,name='change'),
    path('details/<str:pk>/',views.extract_details,name='extract'),
    path('guest_dashboard/',views.guest_dashboard,name='guest_dashboard'),
    path('Housekeeping_request/',views.housekeeping_request,name='housekeeping_request'),
    path('Housekeeping/',views.housekeeping,name='housekeeping'),
    path('change_housekeeping/<str:pk>/',views.change_housekeeping,name='change_housekeeping'),



   
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)