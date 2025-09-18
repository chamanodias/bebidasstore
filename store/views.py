from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem, Order, OrderItem
import random
import string

def home(request):
    """Página inicial com produtos em destaque"""
    featured_products = Product.objects.filter(featured=True, available=True)[:8]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    """Lista de produtos com busca e filtros"""
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filtros
    category_filter = request.GET.get('category')
    alcohol_filter = request.GET.get('alcohol_type')
    search_query = request.GET.get('search')
    
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    if alcohol_filter:
        products = products.filter(alcohol_type=alcohol_filter)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_filter,
        'current_alcohol_type': alcohol_filter,
        'search_query': search_query,
        'alcohol_choices': Product.ALCOHOL_CHOICES,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    """Detalhamento do produto"""
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def register(request):
    """Cadastro de usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            login(request, user)
            return redirect('store:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def get_or_create_cart(request):
    """Obtém ou cria carrinho para o usuário"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    return cart

@require_POST
def add_to_cart(request, product_id):
    """Adicionar produto ao carrinho"""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} adicionado ao carrinho!')
    return redirect('store:product_detail', slug=product.slug)

def cart_detail(request):
    """Visualização do carrinho"""
    cart = get_or_create_cart(request)
    
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart_detail.html', context)

@require_POST
def update_cart_item(request, item_id):
    """Atualizar quantidade do item no carrinho"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('store:cart_detail')

@require_POST
def remove_from_cart(request, item_id):
    """Remover item do carrinho"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    messages.success(request, 'Item removido do carrinho!')
    return redirect('store:cart_detail')

@login_required
def checkout(request):
    """Processo de checkout"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('store:cart_detail')
    
    if request.method == 'POST':
        # Gerar número do pedido
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Criar pedido
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_price=cart.get_total_price(),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city'),
        )
        
        # Criar itens do pedido
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
        
        # Limpar carrinho
        cart.items.all().delete()
        
        messages.success(request, f'Pedido {order_number} realizado com sucesso!')
        return redirect('store:order_detail', order_number=order_number)
    
    context = {
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)

@login_required
def order_detail(request, order_number):
    """Detalhes do pedido"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)

@login_required
def order_history(request):
    """Histórico de pedidos do usuário"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)
