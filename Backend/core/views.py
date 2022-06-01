from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView

from core import permissions as my_permissions
from core.models import Room, TimeSlot, Booking, User
from core.serializers import RoomSerializer, TimeSlotsSerializer, BookingSerializer, \
    BookingCreateSerializer, RoomCreateSerializer, UserSerializer, UserRUDSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from . import permissions as my_permissions
import redis
from ratelimiter import SlidingWindowCounterRateLimiter


# Class based View for User Signup API
class Signup(CreateAPIView):
    model = User
    serializer_class = UserSerializer


# Class based View for User Profile Retrieve and Update API
class Profile(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsSelf]
    serializer_class = UserRUDSerializer
    r = redis.Redis(host='localhost', port=6379, db=1)
    pipeline = r.pipeline()
    rate = 1 # 300 requests allowed
    time_window_unit = 'minute' # per hour
    client_id = 'user-100C' # client id 
    ratelimiter = SlidingWindowCounterRateLimiter(clientid=client_id,redispipeline=pipeline,rate = rate,time_window_unit=time_window_unit)


    # Select User object to return / update
    def get_object(self):
        self.client_id = str(self.request.user.id)
        ratelimiter = SlidingWindowCounterRateLimiter(clientid=self.client_id,redispipeline=self.pipeline,rate = self.rate,time_window_unit=self.time_window_unit)
        if ratelimiter.isRequestAllowed(): # Return true if request allowed 
            return get_object_or_404(User.objects.filter(id=self.request.user.id))
        else: print ('You have exceeded your requests per ' , self.time_window_unit)

    # Get queryset
    def get_queryset(self):
        self.id = self.request.user.id
        return User.objects.filter(id=self.request.user.id)


# Class based view for List and Create Room operations
class Rooms(ListCreateAPIView):
    permission_classes = [my_permissions.IsOwnerOrReadOnly, permissions.IsAuthenticated,
                          my_permissions.IsRoomManagerOrReadOnly]

    # Use respective serializer class depending on the type of request
    def get_serializer_class(self):
        if self.request.method == "POST":
            return RoomCreateSerializer
        else:
            return RoomSerializer

    # Return only rooms owned by room manager , return all if user is customer
    def get_queryset(self):
        if self.request.user.is_room_manager:
            return Room.objects.filter(owner=self.request.user)
        else:
            return Room.objects.all()

    # Automatically assign current user as owner of the room
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Class based view for Retrieve, Update and Delete Room operations
class RoomsRUD(RetrieveUpdateDestroyAPIView):
    permission_classes = [my_permissions.IsOwner, permissions.IsAuthenticated, my_permissions.IsRoomManager]

    lookup_url_kwarg = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


# Class based view for List and Create TimeSlot operations
class TimeSlots(ListCreateAPIView):
    permission_classes = [my_permissions.IsRoomOwner, permissions.IsAuthenticated, my_permissions.IsRoomManager]
    serializer_class = TimeSlotsSerializer

    def get_queryset(self):
        return TimeSlot.objects.filter(room_id=self.request.GET.get('room_id', 0))


# Class based view for Retrieve and Delete TimeSlot operations
class TimeSlotsRD(RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsRoomOwner, my_permissions.IsRoomManager]
    lookup_url_kwarg = 'id'
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotsSerializer


# Class based view for List and Create Booking operations
class Bookings(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsBookingOwnerOrRoomOwner,
                          my_permissions.IsCustomerOrRM]

    # Use respective serializer class depending on the type of request
    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer
        return BookingSerializer

    # Return only bookings owned by the customer if user is customer ,
    # return bookings associated with room owned by user if user is room manager
    def get_queryset(self):
        if self.request.user.is_customer:
            return Booking.objects.filter(customer=self.request.user)
        else:
            return Booking.objects.filter(time_slot__room_id__owner=self.request.user)

    # Automatically assign current user as customer of the booking
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# Class based view for Retrieve and Delete Booking operations
class BookingsRD(RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsBookingOwnerOrRoomOwner]
    lookup_url_kwarg = 'id'
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
