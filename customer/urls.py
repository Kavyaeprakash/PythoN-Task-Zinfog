from django.urls import path
from .views import  AddToCartView, CartView, CheckoutView, HomePageView, LoginView, OrderStatusView, PlaceOrderView, ProductListView, RateProductView, SignupView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'), 
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('rate-product/', RateProductView.as_view(), name='rate_product'),
    path('cart/', CartView.as_view(), name='view_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('place-order/', PlaceOrderView.as_view(), name='place_order'),
    path('order-status/', OrderStatusView.as_view(), name='view_order_status')
]