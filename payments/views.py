import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from market.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from payments.cart import Cart
from payments.forms import CartAddItemForm
from payments.models import Item


class HomeListView(generic.ListView):
    template_name = 'payments/index.html'
    model = Item


class ItemDetailView(generic.DetailView):
    template_name = 'payments/detail.html'
    model = Item

    cart_item_form = CartAddItemForm()

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['cart_item_form'] = self.cart_item_form
        return context


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


# ---------------- CART -----------------------
@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'payments/cart_detail.html', {'cart': cart})
