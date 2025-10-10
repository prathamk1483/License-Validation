from django.db import models
from django.contrib.postgres.fields import ArrayField


class Machine(models.Model):
    macAddress = models.CharField(max_length=64, unique=True)
    os = models.CharField(max_length=64)
    brandName=models.CharField(max_length=64, null=True, blank=True)
    modelName= models.CharField(max_length=64, null=True, blank=True) 
    isActive=models.BooleanField(default=False) 
    def __str__(self):
        return self.macAddress


class BusinessOwner(models.Model):
    ownerid = models.CharField(max_length=16,null=False,blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    emails = models.JSONField(default=list, blank=True)
    phones = models.JSONField(default=list, blank=True)  

    def __str__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=128)
    appId = models.SlugField(unique=True,max_length=32,null=True,blank=True)

    def __str__(self):
        return self.name

    
class License(models.Model):
    licenseKey = models.SlugField(max_length=64, unique=True)
    validTill = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=False)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='licenses')
    business = models.ForeignKey('ClientBusiness', on_delete=models.PROTECT, related_name='licenses', null=True, blank=True)

    def __str__(self):
        return f"{self.licenseKey} ({self.app.name})"


class ClientBusiness(models.Model):
    name = models.CharField(max_length=256)
    businessId = models.SlugField(unique=True, max_length=32)
    domain = models.CharField(max_length=128, null=True, blank=True)
    machines = models.ManyToManyField(Machine, blank=True, related_name='businesses')
    owner = models.ManyToManyField(BusinessOwner, blank=True, related_name='businesses')
    appsOwned = models.ManyToManyField(App, blank=True, related_name='owned_by_businesses')
    ownedLicensesList = models.ManyToManyField('License', blank=True, related_name='owned_by_businesses')

    def __str__(self):
        return self.name




