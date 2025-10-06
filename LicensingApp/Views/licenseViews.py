from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import License
from ..Utils.idGenerator import createId
from django.utils import timezone
from datetime import timedelta
from .. models import App
from ..models import License, ClientBusiness

@api_view(['GET'])
def getLicenseByKey(request):
    """
    Retrieve license details by its licenseKey.
    Example:
        GET /license/readbyid/?licenseKey=<key>
    """
    # Handle both GET param and fallback for request.data (for flexibility)
    licenseKey = request.GET.get("licenseKey") or request.data.get("licenseKey")
    
    if not licenseKey:
        return JsonResponse({"error": "licenseKey parameter is required"}, status=400)

    try:
        license = License.objects.select_related('app', 'business').get(licenseKey=licenseKey)
    except License.DoesNotExist:
        return JsonResponse({"error": f"No license found with key: {licenseKey}"}, status=404)

    # Serialize license details
    license_data = {
        "licenseKey": license.licenseKey,
        "appName": license.app.name,
        "appId": license.app.appId,
        "business": {
            "name": license.business.name,
            "businessId": license.business.businessId,
        } if license.business else None,
        "isActive": license.isActive,
        "validTill": license.validTill.isoformat() if license.validTill else None
    }

    return JsonResponse(license_data, status=200)

@api_view(['GET'])
def getAllLicenses(request):
    licenses = License.objects.all()
    license_list = [{
        "key": license.licenseKey, 
        "appName": license.app.name,
        "appId": license.app.appId,
        "business": license.business.name if license.business else None,
        "validTill": license.validTill,
        "isActive": license.isActive
    } for license in licenses]
    
    return JsonResponse(license_list, safe=False)

@api_view(['POST','GET'])
def createLicense(request):
    url = "http://localhost:8000/app/readbyid/"

    if request.method == "POST":
        appId = request.data.get("appId")
        data = {
            "appId": appId
        }
        try:
            app_instance = App.objects.get(appId=appId)
        except App.DoesNotExist:
            return JsonResponse({"error": f"No App found with appId: {appId}"}, status=404)
        
        key=createId("License")
        validTill = request.data.get("validTill")
        if validTill is None or validTill == "":
            validTill = timezone.now() + timedelta(days=15)

        License.objects.create(
            licenseKey = key,
            validTill=validTill,
            app = app_instance,
        )
        
    return JsonResponse({"message":"Create new License"})

@api_view(['PATCH', 'POST'])
def updateLicense(request):
    params=[]
    licenseKey = request.data.get("licenseKey")
    if not licenseKey:
        return JsonResponse({"error": "licenseKey is required"}, status=400)

    try:
        license = License.objects.get(licenseKey=licenseKey)
    except License.DoesNotExist:
        return JsonResponse({"error": f"No license found with key: {licenseKey}"}, status=404)

    # Update fields if provided
    isActive = request.data.get("isActive")
    if isActive is not None and (isActive == True or isActive == False):
        license.isActive = bool(isActive)
        params.append("activity status")

    validTill = request.data.get("validTill")
    if validTill:
        try:
            license.validTill = timezone.datetime.fromisoformat(validTill)
            params.append("validity")
        except ValueError:
            return JsonResponse({"error": "Invalid validTill format, must be ISO format"}, status=400)

    businessId = request.data.get("businessId")
    if businessId:
        try:
            business = ClientBusiness.objects.get(businessId=businessId)
            license.business = business
        except ClientBusiness.DoesNotExist:
            return JsonResponse({"error": f"No business found with businessId: {businessId}"}, status=404)

    paramsString = str([p for p in params])
    license.save()

    return JsonResponse({
        "message": "License's parameters : " + paramsString + "\nupdated successfully.",
        "licenseKey": license.licenseKey,
        "app": license.app.name,
        "business": license.business.name if license.business else None,
        "isActive": license.isActive,
        "validTill": license.validTill
    })


@api_view(["DELETE"])
def deleteLicense(request):
    if request.method == "DELETE":
        key = request.data.get("licenseKey")
        try:
            licenseToDelete = App.objects.filter(licenseKey=key)
        except License.DoesNotExist:
            return JsonResponse({"message":f"App with id:{key} does not exist"})
        
        licenseToDelete.delete()

        return JsonResponse({"message":f"License with key:{key} deleted Sucessfully"})

    return JsonResponse({"message":"You can delete your License and all it's related Data."})