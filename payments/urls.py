from django.urls import path
from payments.views import (
    AllItemsView, ItemView, ItemBuyView, SuccessPayView, CancelPayView,
    OrderListView, add_to_order, OrderPaymentView, StripeIntentView
)


urlpatterns = [
    path('', AllItemsView.as_view(), name="home"),
    path('item/<int:pk>', ItemView.as_view(), name="view_item"),
    path('buy/<int:pk>', ItemBuyView.as_view(), name="buy_item"),
    path('success/', SuccessPayView.as_view(), name="success_pay"),
    path('cancel/', CancelPayView.as_view(), name="cancel_pay"),
    path('orders/', OrderListView.as_view(), name="orders_list"),
    path('add_to_order/', add_to_order, name="add_to_order"),
    path('order/<int:pk>/', OrderPaymentView.as_view(), name="view_order"),
    path('create-payment-intent/<int:pk>/',
         StripeIntentView.as_view(), name='create-payment-intent'),
]
