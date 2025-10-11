from django.contrib import admin
from django.urls import path
from ..Utils.activityUpdater import deactivateExpiredLicenses

urlpatterns = [
    path("deactivateExpiredLicenses/",deactivateExpiredLicenses,name="updateIsActiveStatus")
]

