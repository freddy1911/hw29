from django.urls import path
from rest_framework.routers import SimpleRouter

from ads.Views.ad import *

router = SimpleRouter()
router.register('', AdViewSet)

urlpatterns = [
    path('<int:pk>/upload_image/', ImageUploadView.as_view())]

urlpatterns += router.urls
