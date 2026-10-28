from django.contrib import admin
from .models import Product, Sale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "quantity", "low_stock_threshold")
    search_fields = ("name", "sku", "category")
    list_filter = ("category",)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "unit_price", "total_amount", "sold_by", "sold_at")
    list_filter = ("sold_at",)
