from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from .Utils import logger

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

@api_view(["GET"])
def validation(request):
    license_key = request.data.get('license') or request.GET.get('license')
    mac = request.GET.get("macAddress") or request.data.get('macAddress')
    clientBusinessId = request.GET.get("clientId") or request.data.get('clientId')
    
    isValid = False
    if not(license_key and mac and clientBusinessId):
        logger.log("INFO","License Validation","Validation View",mac,False,"Missing License or mac or clientID")
        return JsonResponse({"valid": isValid,"message":"Enter license, mac and clientID"})

    data = {
        "businessId":clientBusinessId
    }
    response = requests.get("https://orconixlicensevalidation.vercel.app/clientbusiness/readbyid/",data)
    response = response.json()
    
    machineIsValid = False
    
    for machine in response["machines"]:
        if machine["macAddress"].lower() == mac.replace(':','-').lower() and machine["isActive"]:
            machineIsValid = True
            break

    if not machineIsValid:
        logger.log("INFO","License Validation","Validation View",mac,False,"Machine is not Valid/Inactive")
        return JsonResponse({"valid": False, "message":"Your machine is not registered or is inactive"})
    
    licenseIsValid = False
    for license in response["ownedLicenses"]:
        if license["licenseKey"] == license_key and license["isActive"]:
            licenseIsValid = True
            break

    if not licenseIsValid:
        logger.log("INFO","License Validation","Validation View",mac,False,"License is not Valid/Inactive")
        return JsonResponse({"valid": False, "message":"Your license is inactive"})
    
    isValid = licenseIsValid and machineIsValid

    logger.log("INFO","License Validation","Validation View",mac,True,f"License :{license_key} \nand \nUser:{clientBusinessId} is Valid")
    return JsonResponse({"valid": isValid})