import stripe
import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, View, TemplateView, ListView
from django.conf import settings
from django.shortcuts import render, redirect
from shop.models import Item, Order
from shop.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY

customer = stripe.Customer.create()



products = stripe.Product.list()
prices = stripe.Price.list()

class AllItemsView(ListView):
    """Вывод списка товаров"""
    model = Item
    template_name = "shop/index.html"
    context_object_name = "items"

    def get_queryset(self):
        """Если товар был создан в stripe - создание в БД Django"""
        for prod in products:
            # Приведение цены к float
            price_ = [x for x in prices.data if x.product == prod.id][0]
            price = float(price_.unit_amount / 100)
            # Получить или создать товар
            obj, _ = Item.objects.get_or_create(name=prod.name)
            obj.description = prod.description
            obj.price = price
            obj.save()
        return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context
        
    
class ItemView(DetailView):
    """Детальный просмотр товара"""
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pub_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class ItemBuyView(View):
    """Создание сессии с Stripe для обработки покупки выбранного товара"""
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(pk=item_id)
        domain_url = 'http://localhost:8000/'
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})

        return JsonResponse({'sessionId': checkout_session['id']})


class SuccessPayView(TemplateView):
    """Инфо страница об успешной покупке"""
    template_name = "shop/success.html"


class CancelPayView(TemplateView):
    """Инфо страница об отказе от покупки"""
    template_name = "shop/cancel.html"


def add_to_order(request):
    # Добавить товар в заказ
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect("view_order")
    else:
        form = OrderForm()
    return render(request, "shop/add_to_order.html", {'form': form})


class OrderPaymentView(TemplateView):
    template_name = "shop/order_detail.html"

    def get_context_data(self, **kwargs):
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)
        items = order.items.all()
        stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY
        context = super().get_context_data(**kwargs)
        context.update({
            "items": items,
            "order": order,
            "clientSecret": stripe_pub_key,
            "stripe_pub_key": stripe_pub_key
        })
        return context


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                order_id = self.kwargs["pk"]
                order = Order.objects.get(id=order_id)
                
                # customer = stripe.Customer.create(email=data['email'])
                intent =stripe.PaymentIntent.create(
                    amount=int(order.get_total_price * 100),
                    currency='rub',
                    payment_method_types=["card"],
                    # automatic_payment_methods={
                    #                 'enabled': True,
                    #                 },
                    customer=customer['id'],
                    confirm=True,
                    metadata={
                    "order_id": order.id
                    }
                    )
                return JsonResponse({
                    'clientSecret': intent['client_secret']
                })
            except Exception as e:
                return JsonResponse({'error': str(e)})



        