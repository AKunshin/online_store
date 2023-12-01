from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ItemViewSet, api_create_payment_intent, ItemDetailView


router = DefaultRouter()

router.register(r"items", ItemViewSet)

urlpatterns = [
    path("item-detail/<int:pk>", ItemDetailView.as_view(), name="item-for-buy"),
    path(
        "create_payment_intent/<int:pk>/",
        api_create_payment_intent,
        name="create_payment_intent",
    ),
]

urlpatterns += router.urls