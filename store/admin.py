from django.contrib import admin
from .models import Category, Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Permite ver os itens de uma encomenda diretamente na página da encomenda."""
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_purchase',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'in_stock')
    list_filter = ('category',)
    search_fields = ('title', 'description')

    def in_stock(self, obj):
        return obj.in_stock
    in_stock.boolean = True
    in_stock.short_description = "Em Stock"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_purchase')
