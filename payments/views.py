import stripe
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, View, TemplateView, ListView
from django.conf import settings
from django.shortcuts import render
from shop.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

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