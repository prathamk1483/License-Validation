from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import Machine, ClientBusiness

@api_view(['GET'])
def getMachineByAdd(request):
    mac = request.GET.get('macAddress') or request.data.get('macAddress')
    if not mac:
        return JsonResponse({"error": "macAddress parameter is required"}, status=400)

    try:
        machine = Machine.objects.get(macAddress=mac)
    except Machine.DoesNotExist:
        return JsonResponse({"error": f"No machine found with macAddress: {mac}"}, status=404)

    ownedBy_qs = ClientBusiness.objects.filter(machines=machine).distinct()

    # Serialize businesses
    ownedBy_data = [
        {
            "name": business.name,
            "businessId": business.businessId,
        }
        for business in ownedBy_qs
    ]

    data = {
        "macAddress": machine.macAddress,
        "os": machine.os,
        "brandName": machine.brandName,
        "modelName": machine.modelName,
        "ownedBy": ownedBy_data  # list of businesses
    }

    return JsonResponse(data, status=200)

# Get all machines
@api_view(['GET'])
def getAllMachines(request):
    machines = Machine.objects.all()
    data = [{"macAddress": m.macAddress, "os": m.os,"isActive":m.isActive} for m in machines]
    return JsonResponse(data, safe=False)

# Create a new machine
@api_view(['POST'])
def createMachine(request):
    mac = request.data.get("macAddress")
    os_name = request.data.get("os")
    brandName = request.data.get("brandName","")
    modelName = request.data.get("modelName","")

    if not mac or not os_name:
        return JsonResponse({"error": "macAddress and os are required"}, status=400)

    if Machine.objects.filter(macAddress=mac).exists():
        return JsonResponse({"error": f"Machine with macAddress {mac} already exists"}, status=400)

    machine = Machine.objects.create(
        macAddress=mac, 
        os=os_name,
        brandName=brandName,
        modelName = modelName,
    )
    return JsonResponse({"message": f"Machine {machine.macAddress} created successfully"})

# Update machine information
@api_view(['PATCH', 'POST'])
def updateMachine(request):
    mac = request.data.get("macAddress")
    if not mac:
        return JsonResponse({"error": "macAddress is required"}, status=400)

    try:
        machine = Machine.objects.get(macAddress=mac)
    except Machine.DoesNotExist:
        return JsonResponse({"error": f"No machine found with macAddress: {mac}"}, status=404)

    os_name = request.data.get("os")
    brandName = request.data.get("brandName")
    modelName = request.data.get("modelName")
    isActive = request.data.get("isActive")
    if os_name:
        machine.os = os_name
    if brandName:
        machine.brandName = brandName
    if modelName:
        machine.modelName = modelName
    if isActive and (isActive == 0 or isActive == 1):
        machine.isActive = bool(isActive)

    machine.save()

    return JsonResponse({"message": f"Machine {machine.macAddress} updated successfully"})


@api_view(['DELETE'])
def deleteMachine(request):
    mac = request.data.get("macAddress")
    if not mac:
        return JsonResponse({"error": "macAddress is required"}, status=400)

    try:
        machine = Machine.objects.get(macAddress=mac)
    except Machine.DoesNotExist:
        return JsonResponse({"error": f"No machine found with macAddress: {mac}"}, status=404)

    machine.delete()
    return JsonResponse({"message": f"Machine {mac} deleted successfully"})
