from django.urls import path
from ..views import clientBusinessHome
from ..Views.clientBusinessViews import *

urlpatterns = [
    path('',BusinessHome,name='BusinessHome'),
    path('create/',createBusiness,name='createHome'),
    path('update/',updateBusiness,name='updateBusiness'),
    path('delete/',deleteBusiness,name='deleteBusiness'),
    path('read/',getAllBusinesss,name='getAllBusinesss'),
    path('readbyid/',getBusinessById,name='getBusinessById'),
]
