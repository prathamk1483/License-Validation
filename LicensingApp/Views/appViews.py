from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..Utils.idGenerator import createId
from ..models import App
# Create your views here.

@api_view(['GET'])
def getAppById(request):
    if request.method == "GET":
        appId = request.data.get("appId") or request.GET.get("appId")

        if not appId:
            return JsonResponse({"error": "Missing required field: appId"}, status=400)

        try:
            app = App.objects.get(appId=appId)
        except App.DoesNotExist:
            return JsonResponse({"error": f"No App found with appId: {appId}"}, status=404)

        licenses = app.licenses.select_related("business").all()
        unique_businesses = {license.business for license in licenses if license.business is not None }

        business_list = [
            {
                "name": business.name,
                "businessId": business.businessId,
                "domain": business.domain,
            }
            for business in unique_businesses
        ]

        app_data = {
            "name": app.name,
            "appId": app.appId,
            "userBusinesses": business_list,
        }

        return JsonResponse({"app": app_data}, status=200)

    return JsonResponse({"message": "Use GET to fetch app details by ID"})

@api_view(['POST','GET'])
def getAllApps(request):
    if request.method == "GET":
        apps = App.objects.all()
        app_list = [{"name": app.name, "appId": app.appId} for app in apps]
        return JsonResponse(app_list,safe=False)

    return JsonResponse({"message":"Get the name & Ids for all the Apps"})

@api_view(['POST','GET'])
def createApp(request):
    if request.method == "POST":
        appname = request.data.get("name")
        appId = createId("App")
        newApp = App.objects.create(name=appname,appId=appId)

        return JsonResponse({"message":f"New App with \n id : {appId} \n created Sucessfully"})
    
    return JsonResponse({"message":"You can create your app here"})

@api_view(['PATCH','POST'])
def updateApp(request):
    if request.method == "PATCH":
        appId = request.data.get("appId")
        new_name = request.data.get("name")

        if not appId or not new_name:
            return JsonResponse({"error": "Both 'appId' and 'name' are required"}, status=400)

        try:
            app = App.objects.get(appId=appId)
        except App.DoesNotExist:
            return JsonResponse({"error": f"No App found with appId: {appId}"}, status=404)

        app.name = new_name
        app.save()

        return JsonResponse({"message": f"App '{appId}' renamed successfully", "newName": new_name})
    
    return JsonResponse({"message":"You can rename your App"})

@api_view(["DELETE"])
def deleteApp(request):
    if request.method == "DELETE":
        appId = request.data.get("appId")
        try:
            appToDelete = App.objects.filter(appId=appId)
        except App.DoesNotExist:
            return JsonResponse({"message":f"App with id:{appId} does not exist"})
        
        appToDelete.delete()

        return JsonResponse({"message":f"App with id:{appId} all it's related Data deleted Sucessfully"})
    
    return JsonResponse({"message":"You can delete your App and all it's related Data."})