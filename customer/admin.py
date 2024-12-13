from django.contrib import admin

# Register your models here.
from .models import Order, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'rating', 'total_ratings','created_at')
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'created_at', 'status','created_at')
    list_editable = ('status',)
    search_fields = ['user']

admin.site.register(Order, OrderAdmin)