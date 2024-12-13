from django.template.response import TemplateResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import OrderItem, Product, Order, Cart, Address
from .serializers import ProductSerializer
from django.db.models import F
from django.contrib.auth.models import User  
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login



class HomePageView(APIView):
    permission_classes = [AllowAny]  # Ensure the user is authenticated

    def get(self, request):
        products = Product.objects.all()
        product_data = [{"name": product.name, "description": product.description, "price": product.price} for product in products]
        context = {'products': product_data}
        return TemplateResponse(request, 'customer/home.html',context)

class SignupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'customer/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')  
        return render(request, 'customer/signup.html', {'error': 'Invalid data'})
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, 'customer/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            return redirect('product_list')  
        else:
            return render(request, 'customer/login.html', {'error': 'Invalid credentials'})


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return render(request, 'customer/product.html', {'products': serializer.data})


class RateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=400)
        
        product = get_object_or_404(Product, id=product_id)
        rating = request.data.get('rating')

        if not (0 <= float(rating) <= 5):
            return Response({'error': 'Rating must be between 0 and 5'}, status=400)

        product.total_ratings += 1
        product.rating = ((product.rating * (product.total_ratings - 1)) + float(rating)) / product.total_ratings
        product.save()
        return redirect('product_list')


class AddToCartView(APIView):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return redirect('view_cart')

class CheckoutView(APIView):
    def post(self, request):
        product_ids = request.POST.getlist('product_ids')
        selected_products = Product.objects.filter(id__in=product_ids)
        return render(request, 'customer/cart.html', {'cart_products': selected_products})



class PlaceOrderView(APIView):
    def post(self, request):
        product_ids = request.POST.getlist('product_ids')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        address = Address.objects.create(
            user=request.user,
            address_line=address_line,
            city=city,
            postal_code=postal_code
        )
        order = Order.objects.create(user=request.user, address=address)
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            price = product.price
            OrderItem.objects.create(order=order, product=product, price=price)
        return redirect('view_order_status') 


class CartView(APIView):
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, 'customer/cart.html', {'cart_items': cart_items})

class OrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        order_data = []
        for order in orders:
            items = OrderItem.objects.filter(order=order)
            order_info = {
                'order_id': order.id,
                'status': order.status, 
                'items': [
                    {
                        'product_name': item.product.name,
                        'quantity': item.quantity,
                        'price': item.price
                    } for item in items
                ],
                'total_amount': sum(item.price * item.quantity for item in items)
            }
            order_data.append(order_info)

        return render(request, 'customer/orders.html', {'orders': order_data})
