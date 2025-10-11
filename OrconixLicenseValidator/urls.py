from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('LicensingApp.UrlsHandler.urls')),
    path('app/',include('LicensingApp.UrlsHandler.appUrls')),
    path('license/',include('LicensingApp.UrlsHandler.licenseUrls')),
    path('machine/',include('LicensingApp.UrlsHandler.machineUrls')),
    path('owner/',include('LicensingApp.UrlsHandler.ownerUrls')),
    path('clientbusiness/',include('LicensingApp.UrlsHandler.clientBusinessUrls')),
    path('utils/',include('LicensingApp.UrlsHandler.utilsUrls')),
    path('validateLicense/',include('LicensingApp.urls')),
]