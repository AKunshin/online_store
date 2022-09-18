from rest_framework import routers
from shop import api_views


router = routers.DefaultRouter()
router.register(r'items', api_views.ItemViewSet)

urlpatterns = router.urls