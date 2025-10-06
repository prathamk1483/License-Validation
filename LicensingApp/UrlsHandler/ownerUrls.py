from django.urls import path
from ..views import ownerHome
from ..Views.ownerViews import *

urlpatterns = [
    path('',ownerHome,name='ownerHome'),
    path('create/',createOwner,name='ownerHome'),
    path('readbyId/',getOwnerById,name='ownerHome'),
    path('read/',getAllOwners,name='ownerHome'),
    path('update/',updateOwner,name='ownerHome'),
    path('delete/',deleteOwner,name='ownerHome'),
]

