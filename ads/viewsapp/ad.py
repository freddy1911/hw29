from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
# from psycopg2 import IntegrityError, DatabaseError
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad
from ads.serializers import AdSerializer, AdDetailSerializer, AdListSerializer


class AdPagination(PageNumberPagination):
    page_size = 5


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')
    default_serializer = AdSerializer
    serializer_classes = {
        'retrieve': AdDetailSerializer,
        'list': AdListSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse(
            {
                "name": self.object.name,
                "image": self.object.image.url
            }
        )
