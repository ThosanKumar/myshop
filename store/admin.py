from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price','stock')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','status','total','created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity')
