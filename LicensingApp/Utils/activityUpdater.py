from ..models import License
from datetime import  timezone
from django.http import JsonResponse

def deactivateExpiredLicenses(request):
    """
    View to set isActive=False for all licenses where validTill <= current time.
    Can be triggered manually or by a scheduled request (cron, Vercel task, etc.)
    """
    now = timezone.now()

    expired = License.objects.filter(validTill__lte=now, isActive=True)
    expired_count = expired.count()

    # Deactivate all in one query
    expired.update(isActive=False)

    return JsonResponse({"message" : "Success"})

    