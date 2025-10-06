from django.urls import path
from ..views import licenseHome
from ..Views.licenseViews import *

urlpatterns = [
    path('',licenseHome,name='licenseHome'),
    path('create/',createLicense,name='createHome'),
    path('update/',updateLicense,name='updateLicense'),
    path('delete/',deleteLicense,name='deleteLicense'),
    path('read/',getAllLicenses,name='getAllLicenses'),
    path('readbyid/',getLicenseByKey,name='getLicenseByKey'),
]

