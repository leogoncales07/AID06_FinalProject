from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'price', 'stock', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Comic'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://exemplo.com/imagem.jpg'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("O preço deve ser superior a zero.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("O stock não pode ser negativo.")
        return stock
