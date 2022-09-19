import stripe
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, View
from django.conf import settings
from shop.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

products = stripe.Product.list()
prices = stripe.Price.list()


def sync_products_view(request):
    '''Синхронизация товаров с stripe в БД'''
    print(products)
    print(prices)
    # Приведение цены к float
    for prod in products:
        price_ = [x for x in prices.data if x.product == prod.id][0]
        price = float(price_.unit_amount / 100)
        print(price)

        obj, _ = Item.objects.get_or_create(name=prod.name)
        obj.description = prod.description
        obj.price = price
        obj.save()
    return HttpResponse("data")

class ItemView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pub_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context



class ItemBuyView(View):
    def create_checkout_session(request, item_id):
        item = Item.objects.get(pk=item_id)
        domain_url = 'http://localhost:8000/'
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success.html',
                cancel_url=domain_url + 'cancel.html',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                'price_data': {
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price
                },
                'quantity': 1,
                }],
                # line_items=[
                #     {
                #         'name': item.name,
                #         'amount': item.price,
                #     }
                # ]
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})

        return JsonResponse({'sessionId': checkout_session['id']})