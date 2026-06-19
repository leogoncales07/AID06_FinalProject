from django.urls import path
from . import views

urlpatterns = [
    # --- ÁREA PÚBLICA (LOJA) ---
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Carrinho e Checkout (Público)
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Histórico de Encomendas do Cliente (Público, requer login normal)
    path('orders/', views.order_history, name='order_history'),

    # --- ÁREA RESTRITA (PAINEL DE ADMINISTRAÇÃO) ---
    path('dashboard/', views.DashboardHomeView.as_view(), name='dashboard_home'),
    
    # Gestão de Produtos no Dashboard
    path('dashboard/products/', views.AdminProductListView.as_view(), name='admin_product_list'),
    path('dashboard/products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('dashboard/products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('dashboard/products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Gestão de Encomendas no Dashboard
    path('dashboard/orders/', views.AdminOrderListView.as_view(), name='admin_order_list'),
]
