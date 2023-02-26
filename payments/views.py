import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from market.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, STRIPE_ENDPOINT_SECRET, DOMAIN_URL
from payments.cart import Cart
from payments.forms import CartAddItemForm, OrderCreateForm
from payments.models import Item, OrderItem, Order


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


# ---------- STRIPE ----------
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
def create_checkout_session(request, order_id):
    if request.method == 'GET':
        domain_url = DOMAIN_URL
        stripe.api_key = STRIPE_SECRET_KEY
        try:
            order = Order.objects.get(pk=order_id)
            order_items = OrderItem.objects.filter(order=order_id)

            if request.user != order.user:
                return JsonResponse({'error': f'Order {order_id} is not exist!'})

            line_items = []
            for item in order_items:
                line_items.append({
                        'price_data': {
                            'currency': 'USD',
                            'product_data': {'name': item.item},
                            'unit_amount_decimal': item.price*100,
                            },
                        'quantity': item.quantity,
                        })
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items
            )
            order.checkout_session = checkout_session.get('id')
            order.save()
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session_id = event['data']['object']['id']
        order = Order.objects.get(checkout_session=session_id)
        order.paid = True
        order.save()
    return HttpResponse(status=200)


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
    return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'payments/cart_detail.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if not len(cart):
        return redirect('index')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            order = form.save()
            for it in cart:
                OrderItem.objects.create(order=order,
                                         item=it['item'],
                                         price=it['price'],
                                         quantity=it['quantity'])

            cart.clear()
            return render(request, 'payments/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'payments/order_create.html', {'cart': cart, 'form': form})

