from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import *

router = SimpleRouter()
router.register('location', LocationViewSet)

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
]

urlpatterns += router.urls
