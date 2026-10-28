from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import ProductForm, SaleForm
from .models import Product, Sale


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard")
    return render(request, "inventory/login.html", {"form": form})


@login_required
def dashboard(request):
    products = Product.objects.all()
    stock_value = sum((p.stock_value for p in products), Decimal("0.00"))
    total_sales = Sale.objects.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
    context = {
        "product_count": products.count(),
        "units_in_stock": sum(p.quantity for p in products),
        "stock_value": stock_value,
        "total_sales": total_sales,
        "low_stock_products": products.filter(quantity__lte=F("low_stock_threshold"))[:6],
        "recent_sales": Sale.objects.select_related("product", "sold_by")[:5],
    }
    return render(request, "inventory/dashboard.html", context)


@login_required
def product_list(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q) | products.filter(sku__icontains=q)
    return render(request, "inventory/product_list.html", {"products": products.distinct(), "q": q})


@login_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product added successfully.")
        return redirect("product_list")
    return render(request, "inventory/product_form.html", {"form": form, "title": "Add Product"})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect("product_list")
    return render(request, "inventory/product_form.html", {"form": form, "title": "Edit Product"})


@login_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.sales.exists():
        messages.error(request, "This product has sales history and cannot be deleted.")
    else:
        product.delete()
        messages.success(request, "Product deleted.")
    return redirect("product_list")


@login_required
def record_sale(request):
    form = SaleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product_id = form.cleaned_data["product"].pk
        qty = form.cleaned_data["quantity"]
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=product_id)
            if qty > product.quantity:
                form.add_error("quantity", f"Only {product.quantity} unit(s) are currently available.")
            else:
                unit_price = product.price
                total = unit_price * qty
                Sale.objects.create(
                    product=product, quantity=qty, unit_price=unit_price,
                    total_amount=total, sold_by=request.user
                )
                product.quantity -= qty
                product.save(update_fields=["quantity"])
                messages.success(request, f"Sale recorded. Total: ₹{total:.2f}. Stock updated.")
                return redirect("sales_history")
    return render(request, "inventory/sale_form.html", {"form": form})


@login_required
def sales_history(request):
    sales = Sale.objects.select_related("product", "sold_by")
    total_sales = sales.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
    return render(request, "inventory/sales_history.html", {"sales": sales, "total_sales": total_sales})
