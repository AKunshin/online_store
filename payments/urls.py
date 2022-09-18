from django.urls import path
from .views import ItemView, ItemBuyView


urlpatterns = [
    path('item/<int:pk>/', ItemView.as_view(), name="view_item"),
    path('buy/<int:pk>/', ItemBuyView.as_view(), name="buy_item"),
]