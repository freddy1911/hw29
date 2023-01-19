

from django.http import JsonResponse


# Create your views here.


def root(request):
    return JsonResponse({"status": "ok"})
