from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import ItemViewSet, api_create_payment_intent


router = SimpleRouter()

router.register(r"item", ItemViewSet)

urlpatterns = [
    path(
        "create_payment_intent/<int:pk>/",
        api_create_payment_intent,
        name="create_payment_intent",
    ),
]

urlpatterns += router.urls