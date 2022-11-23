from django.urls import path
from payments.views import *


urlpatterns = [
    path('', AllItemsView.as_view(), name="home"),
    path('item/<int:pk>', ItemView.as_view(), name="view_item"),
    path('buy/<int:pk>', ItemBuyView.as_view(), name="buy_item"),
    path('<int:pk>', ItemBuyView.as_view(), name="buy_item"),
    path('success/', SuccessPayView.as_view(), name="success_pay"),
    path('cancel/', CancelPayView.as_view(), name="cancel_pay"),
    path('add_to_order/', add_to_order, name="add_to_order"),
    path('order/<int:pk>', OrderPaymentView.as_view(), name='order_view'),
    path('create-payment-intent/<int:pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
]
