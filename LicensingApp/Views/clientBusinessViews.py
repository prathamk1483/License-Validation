from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import ClientBusiness, BusinessOwner, Machine , App, License
from django.utils import timezone
from ..Utils.idGenerator import createId

# Home / simple message
@api_view(['GET'])
def BusinessHome(request):
    return JsonResponse({"message": "Welcome to the ClientBusiness API"})


# Create a new business
@api_view(['POST'])
def createBusiness(request):
    data = request.data
    name = data.get("name")
    businessId = createId("Business")
    domain = data.get("domain","")
    owner_ids = data.get("ownerIds", [])
    machine_ids = data.get("machineIds", []) 

    if not all([name, businessId]):
        return JsonResponse({"error": "name is required"}, status=400)

    business = ClientBusiness.objects.create(name=name, businessId=businessId, domain=domain)

    if owner_ids:
        owners = BusinessOwner.objects.filter(id__in=owner_ids)
        business.owner.add(*owners)

    if machine_ids:
        machines = Machine.objects.filter(id__in=machine_ids)
        business.machines.add(*machines)

    return JsonResponse({"message": f"Business '{name}' created successfully", "businessId": business.businessId})


# Update a business
@api_view(['PATCH', 'POST'])
def updateBusiness(request):
    data = request.data
    businessId = data.get("businessId")
    ownerIds=data.get("ownerIds",[])
    machineIds=data.get("machineIds",[])
    appIds = data.get("ownedApps",[])
    ownsLicenses = data.get("Licenses",[])
    machineIds = data.get("machines",[])
    if not businessId:
        return JsonResponse({"error": "businessId is required"}, status=400)

    try:
        business = ClientBusiness.objects.get(businessId=businessId)
    except ClientBusiness.DoesNotExist:
        return JsonResponse({"error": f"No business found with id: {businessId}"}, status=404)

    if "name" in data:
        business.name = data["name"]
    if "domain" in data:
        business.domain = data["domain"]
    if "ownerIds" in data:
        owners = BusinessOwner.objects.filter(ownerid__in=ownerIds)
        business.owner.set(owners)
    if "machines" in data:
        machines = Machine.objects.filter(macAddress__in=machineIds)
        business.machines.set(machines)
        print(f"{business.name} owns {machines}")
    if "ownedApps" in data:
        apps = App.objects.filter(appId__in=appIds)
        business.appsOwned.set(apps)
    if "Licenses" in data:
        licenses = License.objects.filter(licenseKey__in=ownsLicenses)
        for l in licenses:
            l.business = business
            l.save()
        business.ownedLicensesList.set(licenses)

    business.save()
    return JsonResponse({"message": f"Business '{businessId}' updated successfully"})


# Delete a business
@api_view(['DELETE'])
def deleteBusiness(request):
    data = request.data
    businessId = data.get("businessId")
    if not businessId:
        return JsonResponse({"error": "businessId is required"}, status=400)

    try:
        business = ClientBusiness.objects.get(businessId=businessId)
    except ClientBusiness.DoesNotExist:
        return JsonResponse({"error": f"No business found with id: {businessId}"}, status=404)
    bname = business.name
    business.delete()
    return JsonResponse({"message": f"Business '{bname}' with id :{businessId} deleted successfully"})


# Get all businesses
@api_view(['GET'])
def getAllBusinesss(request):
    businesses = ClientBusiness.objects.all()
    business_list = []
    for b in businesses:
        business_list.append({
            "name": b.name,
            "businessId": b.businessId,
            "domain": b.domain,
            "owners": [owner.name for owner in b.owner.all()],
            "machines": [machine.macAddress for machine in b.machines.all()]
        })
    return JsonResponse(business_list, safe=False)

@api_view(['GET'])
def getBusinessById(request):
    businessId = request.GET.get("businessId") or request.data.get("businessId")
    print("Received businessID :",businessId)
    if not businessId:
        return JsonResponse({"error": "businessId parameter is required"}, status=400)

    try:
        business = ClientBusiness.objects.prefetch_related(
            'owner', 'machines', 'appsOwned', 'ownedLicensesList'
        ).get(businessId=businessId)
    except ClientBusiness.DoesNotExist:
        return JsonResponse({"error": f"No business found with id: {businessId}"}, status=404)

    # Owners
    owners_data = [
        {
            "name": owner.name,
            "id": owner.ownerid
        }
        for owner in business.owner.all()
    ]

    # Machines
    machines_data = [
        {
            "macAddress": machine.macAddress,
            "os": machine.os,
            "brandName": machine.brandName,
            "modelName": machine.modelName,
            "isActive": machine.isActive,
        }
        for machine in business.machines.all()
    ]

    # Owned Apps
    owned_apps_data = [
        {
            "name": app.name,
            "id" : app.appId
        }
        for app in business.appsOwned.all()  # <— Use .all() on M2M
    ]

    # Owned Licenses
    owned_licenses_data = [
        {
            "licenseKey": license.licenseKey,
            "isActive" :license.isActive,
        }
        for license in business.ownedLicensesList.all()
    ]

    business_data = {
        "name": business.name,
        "businessId": business.businessId,
        "domain": business.domain,
        "owners": owners_data,
        "machines": machines_data,
        "ownedApps": owned_apps_data,
        "ownedLicenses": owned_licenses_data
    }

    return JsonResponse(business_data, status=200)
