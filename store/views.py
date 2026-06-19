from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Count, F
from .models import Product, Order, OrderItem, Category
from .forms import ProductForm

# ==========================================
# --- 1. VISTAS PÚBLICAS (Loja / Clientes) ---
# ==========================================

class ProductListView(ListView):
    """Montra Pública: Lista os comics disponíveis para clientes normais."""
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        
        if query:
            queryset = queryset.filter(title__icontains=query)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    """Página de Detalhe de um único comic (Pública)."""
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

# --- CARRINHO DE COMPRAS E CHECKOUT ---

def add_to_cart(request, product_id):
    """Adiciona um produto ao carrinho (Sessão)."""
    product = get_object_or_404(Product, pk=product_id)
    
    if product.stock <= 0:
        messages.error(request, f"Desculpe, {product.title} está esgotado.")
        return redirect('product_detail', pk=product_id)
        
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        if cart[product_id_str]['quantity'] < product.stock:
            cart[product_id_str]['quantity'] += 1
            messages.success(request, f"Adicionaste mais um {product.title} ao carrinho.")
        else:
            messages.warning(request, f"Não podes adicionar mais {product.title}. Limite de stock atingido.")
    else:
        cart[product_id_str] = {
            'title': product.title,
            'price': str(product.price),
            'quantity': 1
        }
        messages.success(request, f"{product.title} adicionado ao carrinho.")
        
    request.session['cart'] = cart
    return redirect('product_list')

def view_cart(request):
    """Visualizar itens no carrinho."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, item_data in cart.items():
        subtotal = float(item_data['price']) * item_data['quantity']
        total += subtotal
        cart_items.append({
            'product_id': product_id,
            'title': item_data['title'],
            'price': item_data['price'],
            'quantity': item_data['quantity'],
            'subtotal': subtotal
        })
        
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'store/cart.html', context)

def clear_cart(request):
    """Esvazia o carrinho."""
    if 'cart' in request.session:
        del request.session['cart']
        messages.success(request, "O carrinho foi esvaziado.")
    return redirect('view_cart')

@login_required
@transaction.atomic
def checkout(request):
    """Cria a encomenda do utilizador, deduz o stock e limpa o carrinho."""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, "O seu carrinho está vazio.")
        return redirect('product_list')
        
    total_amount = sum(float(item['price']) * item['quantity'] for item in cart.values())
    
    order = Order.objects.create(
        customer=request.user,
        status='pago',
        total_amount=total_amount
    )
    
    for product_id_str, item_data in cart.items():
        product = get_object_or_404(Product, pk=int(product_id_str))
        quantity_ordered = item_data['quantity']
        
        if product.stock < quantity_ordered:
            messages.error(request, f"Erro: Stock insuficiente para {product.title}.")
            transaction.set_rollback(True)
            return redirect('view_cart')
            
        product.stock -= quantity_ordered
        product.save()
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity_ordered,
            price_at_purchase=product.price
        )
        
    del request.session['cart']
    messages.success(request, f"Compra finalizada com sucesso! Encomenda #{order.id}.")
    return render(request, 'store/checkout_success.html', {'order': order})

@login_required
def order_history(request):
    """O Cliente vê o seu próprio histórico de compras."""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


# ====================================================
# --- 2. VISTAS RESTRITAS (Painel de Administração) ---
# ====================================================

class StaffRequiredMixin(UserPassesTestMixin):
    """Bloqueio Total: Apenas o leo, max e theo (staff) conseguem entrar."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class DashboardHomeView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """Resumo Geral do Painel de Administração."""
    template_name = 'store/dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Estatísticas Rápidas
        context['total_products'] = Product.objects.count()
        context['low_stock_products'] = Product.objects.filter(stock__lte=3)
        context['total_orders'] = Order.objects.count()
        
        # Calcular total faturado
        revenue = Order.objects.aggregate(total=Sum('total_amount'))['total']
        context['total_revenue'] = revenue if revenue else 0.00
        
        return context

class AdminProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Tabela Administrativa de Inventário de Produtos."""
    model = Product
    template_name = 'store/dashboard/product_manage_list.html'
    context_object_name = 'products'
    
class AdminOrderListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Tabela Administrativa de TODAS as vendas da loja."""
    model = Order
    template_name = 'store/dashboard/order_manage_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

# --- CRUD de Produtos no Painel ---

class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('admin_product_list') # Volta para a tabela admin
    
    def form_valid(self, form):
        messages.success(self.request, "Produto criado com sucesso.")
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('admin_product_list') # Volta para a tabela admin
        
    def form_valid(self, form):
        messages.success(self.request, "Produto atualizado com sucesso.")
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('admin_product_list') # Volta para a tabela admin
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Produto apagado com sucesso.")
        return super().delete(request, *args, **kwargs)
