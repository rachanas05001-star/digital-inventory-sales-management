from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "sku", "price", "quantity", "low_stock_threshold"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Notebook"}),
            "category": forms.TextInput(attrs={"placeholder": "e.g. Stationery"}),
            "sku": forms.TextInput(attrs={"placeholder": "Unique code, e.g. NOTE-001"}),
            "price": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"min": "0"}),
            "low_stock_threshold": forms.NumberInput(attrs={"min": "0"}),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class SaleForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.none(), empty_label="Choose a product")
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"min": "1"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(quantity__gt=0).order_by("name")
