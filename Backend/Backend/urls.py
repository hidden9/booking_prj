"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework.authtoken.views import obtain_auth_token
from core import views as views

urlpatterns = [
    path('admin/', admin.site.urls),

    # login
    path('api/login', obtain_auth_token, name="login"),
    path('api/signup', views.Signup.as_view(), name="signup"),
    path('api/profile', views.Profile.as_view(), name="profile"),
    
    # room booking
    path('api/rooms', views.Rooms.as_view(), name="rooms"),
    path('api/rooms/<int:id>', views.RoomsRUD.as_view(), name="rooms_rud"),
    path('api/timeslots', views.TimeSlots.as_view(), name="timeslots"),
    path('api/timeslots/<int:id>', views.TimeSlotsRD.as_view(), name="timeslots_rd"),
    path('api/bookings', views.Bookings.as_view(), name="bookings"),
    path('api/bookings/<int:id>', views.BookingsRD.as_view(), name="bookings_rd"),
]
