from rest_framework.routers import SimpleRouter

from users.views import LocationViewSet

router = SimpleRouter()
router.register('loc', LocationViewSet)

