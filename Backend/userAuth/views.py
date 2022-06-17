from http.client import HTTPResponse
from mimetypes import init
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404

from userAuth.models import User
from userAuth.serializers import UserSerializer, UserRUDSerializer
from . import permissions as my_permissions
#from throttle.decorators import throttle
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

# from userAuth.ratelimiter import SlidingWindowCounterRateLimiter
#import redis





# Class based View for User Signup API
class Signup(CreateAPIView):
    model = User
    serializer_class = UserSerializer


# Class based View for User Profile Retrieve and Update API
class Profile(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsSelf]
    serializer_class = UserRUDSerializer
    # r = redis.Redis(host='localhost', port=6379, db=1)
    # pipeline = r.pipeline()
    # rate = 1 # 300 requests allowed
    # time_window_unit = 'minute' # per hour
    # client_id = 'user-100C' # client id 
    # ratelimiter = SlidingWindowCounterRateLimiter(clientid=client_id,redispipeline=pipeline,rate = rate,time_window_unit=time_window_unit)


    # @method_decorator(throttle(zone='default'))
    # def dispatch(self, *args, **kwargs):
    #     return super(Profile, self).dispatch(*args, **kwargs)

    # Select User object to return / update
    def get_object(self):
        self.client_id = str(self.request.user.id)
        # ratelimiter = SlidingWindowCounterRateLimiter(clientid=self.client_id,redispipeline=self.pipeline,rate = self.rate,time_window_unit=self.time_window_unit)
        # if ratelimiter.isRequestAllowed(): # Return true if request allowed 
        return get_object_or_404(User.objects.filter(id=self.request.user.id))
        # else: print ('You have exceeded your requests per ' , self.time_window_unit)
            

    # Get queryset
   # @throttle(zone='default')
    def get_queryset(self):
        self.id = self.request.user.id
        return User.objects.filter(id=self.request.user.id)
