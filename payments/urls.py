from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='index'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('config/', stripe_config),
    path('create-checkout-session/<int:order_id>/', create_checkout_session, name='create_checkout_session'),
    path('webhook/', webhook),
    path('success/', success),
    path('cancel/', cancel),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<item_id>/', cart_add, name='cart_add'),
    path('cart/remove/<item_id>/', cart_remove, name='cart_remove'),
    path('order/create/', order_create, name='order_create'),
]