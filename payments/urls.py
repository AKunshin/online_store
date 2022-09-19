from django.urls import path
from .views import ItemView, sync_products_view, ItemBuyView


urlpatterns = [
    path('', sync_products_view),
    path('item/<int:pk>/', ItemView.as_view(), name="view_item"),
    path('buy/<int:pk>/', ItemBuyView.as_view(), name="buy_item"),
]