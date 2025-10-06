from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import ClientBusiness
import requests
# Create your views here.

@api_view(['POST','GET'])
def home(request):
    return JsonResponse({"message":"Welcome to Orconix's License Validation API."})

@api_view(['POST','GET'])
def appHome(request):
    return JsonResponse({"message":"Welcome to Orconix's License Validation API's App Home"})

@api_view(['POST','GET'])
def licenseHome(request):
    return JsonResponse({"message":"Welcome to Orconix's License Validation API's License Home"})

@api_view(['POST','GET'])
def machineHome(request):
    return JsonResponse({"message":"Welcome to Orconix's License Validation API's Machine Home"})

@api_view(['POST','GET'])
def ownerHome(request):
    return JsonResponse({"message":"Welcome to Orconix's License Validation API's Owner Home"})

@api_view(['POST','GET'])
def clientBusinessHome(request):
    return JsonResponse({"message":"Welcome to Orconix's License Validation API's client Business Home"})

def validation(request):
    license_key = request.GET.get("license") or request.data.get("license")
    mac = request.GET.get("macAddress") or request.data.get("macAddress")
    clientBusinessId = request.GET.get("clientId") or request.data.get("clientId")

    print("Received MAC :",mac)
    isValid = True
    if not(license_key and mac and clientBusinessId):
        return JsonResponse({"valid": isValid})

    data = {
        "businessId":clientBusinessId
    }
    print("Making request to internal API")
    response = requests.get("https://orconixlicensevalidation.vercel.app//clientbusiness/readbyid/",data)
    response = response.json()

    if not (response["businessId"] == clientBusinessId):
        print("Invalid businessID")
        return JsonResponse({"valid": False})
    
    machineFound = False
    
    for machine in response["machines"]:
        print("Found macs :",machine["macAddress"].lower())
        if machine["macAddress"].lower() == mac.replace(':','-'):
            machineFound = True
            break

    if not machineFound:
        return JsonResponse({"valid": False})
    
    licenseFound = False
    for license in response["ownedLicenses"]:
        if license["licenseKey"] == license_key:
            licenseFound = True
            break

    isValid = licenseFound and machineFound 

    return JsonResponse({"valid": isValid})