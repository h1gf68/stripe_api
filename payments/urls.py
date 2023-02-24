from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='index'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('config/', stripe_config),
    path('create-checkout-session/<int:pk>/', create_checkout_session),
    path('success/', success),
    path('cancel/', cancel),
]