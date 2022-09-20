from django.urls import path
from payments.views import *


urlpatterns = [
    path('', AllItemsView.as_view(), name="home"),
    path('item/<int:pk>', ItemView.as_view(), name="view_item"),
    path('buy/<int:pk>', ItemBuyView.as_view(), name="buy_item"),
    path('success/', SuccessPayView.as_view(), name="success_pay"),
    path('cancel/', CancelPayView.as_view(), name="cancel_pay"),
]
