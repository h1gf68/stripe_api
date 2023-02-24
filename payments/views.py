import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from market.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from payments.models import Item


class HomeListView(generic.ListView):
    template_name = 'payments/index.html'
    model = Item


class ItemDetailView(generic.DetailView):
    template_name = 'payments/detail.html'
    model = Item


def success(request):
    return render(request, 'payments/success.html')


def cancel(request):
    return render(request, 'payments/cancel.html')


@login_required
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@login_required
@csrf_exempt
def create_checkout_session(request, pk):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = STRIPE_SECRET_KEY
        try:
            item = Item.objects.get(pk=pk)
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'USD',
                            'product_data': {
                                'name': item.name,
                                'description': item.description,
                            },
                            'unit_amount_decimal': item.price*100,
                        },
                        # 'price': STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

