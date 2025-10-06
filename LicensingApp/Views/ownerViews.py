from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import BusinessOwner
from ..Utils.idGenerator import createId

# Get owner by ID
@api_view(['GET'])
def getOwnerById(request):
    owner_id = request.data.get("ownerId")
    if not owner_id:
        return JsonResponse({"error": "ownerId parameter is required"}, status=400)

    try:
        owner = BusinessOwner.objects.get(id=owner_id)
    except BusinessOwner.DoesNotExist:
        return JsonResponse({"error": f"No owner found with id: {owner_id}"}, status=404)

    owner_data = {
        "id": owner.id,
        "name": owner.name,
        "emails": [e.email for e in owner.emails.all()],
        "phones": [p.phone for p in owner.phones.all()],
        "businesses": [{"name": b.name, "businessId": b.businessId} for b in owner.businesses.all()]
    }
    return JsonResponse(owner_data)


# Get all owners
@api_view(['GET'])
def getAllOwners(request):
    owners = BusinessOwner.objects.all()
    owner_list = []
    for o in owners:
        owner_list.append({
            "id": o.id,
            "name": o.name,
            "emails": [e.email for e in o.emails.all()],
            "phones": [p.phone for p in o.phones.all()],
            "businesses": [{"name": b.name, "businessId": b.businessId} for b in o.businesses.all()]
        })
    return JsonResponse(owner_list, safe=False)


# Create owner
@api_view(['POST'])
def createOwner(request):
    data = request.data
    name = data.get("name")
    emails = data.get("email", [])  
    phones = data.get("phone", [])  

    print(emails)
    print(phones)

    if not emails:
        return JsonResponse({"error": "At least one email is required"}, status=400)

    owner = BusinessOwner.objects.create(ownerid=createId("Owner"),name=name, emails=emails , phones=phones)


    return JsonResponse({
        # "message" :"Sucess"
        "message": f"Owner '{owner.name}' created successfully",
        "ownerId": owner.ownerid
    })


# Update owner
@api_view(['PATCH', 'POST'])
def updateOwner(request):
    data = request.data
    owner_id = data.get("ownerId")
    if not owner_id:
        return JsonResponse({"error": "ownerId is required"}, status=400)

    try:
        owner = BusinessOwner.objects.get(id=owner_id)
    except BusinessOwner.DoesNotExist:
        return JsonResponse({"error": f"No owner found with id: {owner_id}"}, status=404)

    # Update name
    if "name" in data:
        owner.name = data["name"]
        owner.save()

    # Update emails
    if "email" in data:
        new_emails = data["email"]
        owner.emails.all().delete()  
        for e in new_emails:
            OwnerEmail.objects.create(owner=owner, email=e)

    # Update phones
    if "phone" in data:
        new_phones = data["phone"]
        owner.phones.all().delete() 
        for p in new_phones:
            OwnerPhone.objects.create(owner=owner, phone=p)

    return JsonResponse({"message": f"Owner '{owner_id}' updated successfully"})


# Delete owner
@api_view(["DELETE"])
def deleteOwner(request):
    data = request.data
    owner_id = data.get("ownerId")
    if not owner_id:
        return JsonResponse({"error": "ownerId is required"}, status=400)

    try:
        owner = BusinessOwner.objects.get(id=owner_id)
    except BusinessOwner.DoesNotExist:
        return JsonResponse({"error": f"No owner found with id: {owner_id}"}, status=404)

    # Remove owner from businesses; delete business if no owners left
    for business in owner.businesses.all():
        business.owner.remove(owner)
        if business.owner.count() == 0:
            business.delete()

    # Delete associated emails and phones
    owner.emails.all().delete()
    owner.phones.all().delete()

    # Delete the owner
    owner.delete()
    return JsonResponse({"message": f"Owner '{owner_id}' deleted successfully"})
