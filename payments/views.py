import stripe
from django.http import JsonResponse
from django.views.generic import DetailView, View
from django.conf import settings
from shop.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemView(DetailView):
    model = Item
    # template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pub_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class ItemBuyView(View):
    def create_checkout_session(request, item_id):
        item = Item.objects.get(pk=item_id)
        if request.method == 'GET':
            domain_url = 'http://localhost:8000/'
            try:
                # Create new Checkout Session for the order
                # Other optional params include:
                # [billing_address_collection] - to display billing address details on the page
                # [customer] - if you have an existing Stripe Customer ID
                # [payment_intent_data] - capture the payment later
                # [customer_email] - prefill the email input in the form
                # For full details see https://stripe.com/docs/api/checkout/sessions/create

                # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
                checkout_session = stripe.checkout.Session.create(
                    success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'cancelled/',
                    payment_method_types=['card'],
                    mode='payment',
                    line_items=[
                        {
                            'name': item.name,
                            'quantity': 1,
                            'currency': 'rub',
                            'amount': item.price,
                        }
                    ]
                )
                return JsonResponse({'sessionId': checkout_session['id']})
            except Exception as e:
                return JsonResponse({'error': str(e)})