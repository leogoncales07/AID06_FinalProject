from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Category(models.Model):
    """Categoria / Universo (ex: Marvel, DC Comics, Manga, Image Comics)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Produto (Banda Desenhada / Comic Book) à venda na loja."""
    title = models.CharField(max_length=200, verbose_name="Título")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Categoria"
    )
    description = models.TextField(blank=True, verbose_name="Descrição")
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="O preço deve ser superior a 0.")],
        verbose_name="Preço (€)"
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="O stock não pode ser negativo.")],
        verbose_name="Stock"
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="URL da Imagem da Capa"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def in_stock(self):
        """Verifica se o produto está em stock."""
        return self.stock > 0


class Order(models.Model):
    """Encomenda / Fatura — regista uma compra feita por um utilizador."""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('cancelado', 'Cancelado'),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Cliente"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Encomenda")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Estado"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total (€)"
    )

    class Meta:
        verbose_name = "Encomenda"
        verbose_name_plural = "Encomendas"
        ordering = ['-created_at']

    def __str__(self):
        return f"Encomenda #{self.pk} — {self.customer.username}"


class OrderItem(models.Model):
    """Linha da Fatura — cada produto dentro de uma encomenda."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Encomenda"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Produto"
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1, message="A quantidade deve ser pelo menos 1.")],
        verbose_name="Quantidade"
    )
    price_at_purchase = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Preço na Compra (€)"
    )

    class Meta:
        verbose_name = "Item da Encomenda"
        verbose_name_plural = "Itens da Encomenda"

    def __str__(self):
        return f"{self.quantity}x {self.product.title}"

    @property
    def subtotal(self):
        return self.quantity * self.price_at_purchase
