from django.urls import path
from ..views import appHome
from ..Views.appViews import *

urlpatterns = [
    path('',appHome,name='appHome'),
    path('create/',createApp,name='createApp'),
    path('updatebyid/',updateApp,name='updateApp'),
    path('deletebyid/',deleteApp,name='deleteApp'),
    path('read/',getAllApps,name='getAllApps'),
    path('readbyid/',getAppById,name='getAppById'),
]

