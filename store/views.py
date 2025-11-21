from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
import random
import string
import datetime

def home(request):
    """Página inicial com produtos em destaque (catálogo em memória)"""
    featured_products = [p for p in PRODUCTS if p.get("featured") and p.get("available", True)][:8]
    categories = CATEGORIES
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    """Lista de produtos com busca e filtros (catálogo em memória)"""
    categories = CATEGORIES
    category_filter = request.GET.get('category', '') or ''
    alcohol_filter = request.GET.get('alcohol_type', '') or ''
    search_query = request.GET.get('search', '') or ''
    products = filter_products(category_filter, alcohol_filter, search_query)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_filter,
        'current_alcohol_type': alcohol_filter,
        'search_query': search_query,
        'alcohol_choices': ALCOHOL_CHOICES,
    }
    return render(request, 'store/product_list.html', context)

def category_products(request, slug):
    """Produtos filtrados por categoria (catálogo em memória)"""
    category = get_category_by_slug(slug)
    categories = CATEGORIES
    alcohol_filter = request.GET.get('alcohol_type', '') or ''
    search_query = request.GET.get('search', '') or ''
    products = filter_products(category_slug=slug, alcohol_type=alcohol_filter, search_query=search_query)

    context = {
        'products': products,
        'categories': categories,
        'current_category': slug,
        'current_alcohol_type': alcohol_filter,
        'search_query': search_query,
        'alcohol_choices': ALCOHOL_CHOICES,
        'category': category,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    """Detalhamento do produto (catálogo em memória)"""
    product = get_product_by_slug(slug)
    if not product:
        messages.error(request, 'Produto não encontrado.')
        return redirect('store:product_list')
    related_products = [p for p in PRODUCTS if p.get('available', True) and p['category_slug'] == product['category_slug'] and p['id'] != product['id']][:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def register(request):
    """Cadastro desativado neste modo. Redireciona com mensagem."""
    messages.info(request, 'Cadastro e login estão desativados neste modo de demonstração. Use o checkout sem login.')
    return redirect('store:home')


@require_POST
def add_to_cart(request, product_id):
    """Adicionar produto ao carrinho (sessão)"""
    product = get_product_by_id(product_id)
    if not product or not product.get('available', True):
        messages.error(request, 'Produto indisponível.')
        return redirect('store:product_list')

    quantity = int(request.POST.get('quantity', 1))
    cart = get_session_cart(request)
    # procurar item existente
    found = False
    for it in cart.get('items', []):
        if it['product_id'] == product['id']:
            it['quantity'] = int(it['quantity']) + quantity
            found = True
            break
    if not found:
        cart.setdefault('items', []).append({
            'product_id': product['id'],
            'slug': product['slug'],
            'name': product['name'],
            'description': product.get('description', ''),
            'price': product['price'],
            'quantity': quantity,
            'volume': product.get('volume'),
            'alcohol_type_display': product.get('alcohol_type_display', ''),
            'image_url': product.get('image_url', ''),
        })
    save_session_cart(request, cart)
    messages.success(request, f"{product['name']} adicionado ao carrinho!")
    return redirect('store:product_detail', slug=product['slug'])

def cart_detail(request):
    """Visualização do carrinho (sessão)"""
    cart = get_session_cart(request)
    cart_view = build_cart_context(cart)
    context = {
        'cart_items': cart_view['cart_items'],
        'cart_total_items': cart_view['cart_total_items'],
        'cart_total': cart_view['cart_total'],
    }
    return render(request, 'store/cart_detail.html', context)

@require_POST
def update_cart_item(request, product_id):
    """Atualizar quantidade do item no carrinho (sessão)"""
    cart = get_session_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    new_items = []
    for it in cart.get('items', []):
        if it['product_id'] == product_id:
            if quantity > 0:
                it['quantity'] = quantity
                new_items.append(it)
            # se quantity <= 0, remove item
        else:
            new_items.append(it)
    cart['items'] = new_items
    save_session_cart(request, cart)
    return redirect('store:cart_detail')

@require_POST
def remove_from_cart(request, product_id):
    """Remover item do carrinho (sessão)"""
    cart = get_session_cart(request)
    cart['items'] = [it for it in cart.get('items', []) if it['product_id'] != product_id]
    save_session_cart(request, cart)
    messages.success(request, 'Item removido do carrinho!')
    return redirect('store:cart_detail')

def checkout(request):
    """Processo de checkout (sessão)"""
    cart = get_session_cart(request)
    cart_view = build_cart_context(cart)
    if not cart_view['cart_items']:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('store:cart_detail')

    if request.method == 'POST':
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        now = datetime.datetime.now()
        order = {
            'order_number': order_number,
            'total_price': cart_view['cart_total'],
            'items': cart_view['cart_items'],
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'postal_code': request.POST.get('postal_code'),
            'city': request.POST.get('city'),
            'status': 'confirmado',
            'created_at_str': now.strftime('%d/%m/%Y às %H:%M'),
        }
        orders = request.session.get('orders', [])
        orders.append(order)
        request.session['orders'] = orders
        # Limpar carrinho
        request.session['cart'] = {'items': []}
        request.session.modified = True
        messages.success(request, f"Pedido {order_number} realizado com sucesso!")
        return redirect('store:order_detail', order_number=order_number)

    context = {
        'cart_items': cart_view['cart_items'],
        'cart_total_items': cart_view['cart_total_items'],
        'cart_total': cart_view['cart_total'],
    }
    return render(request, 'store/checkout.html', context)

def order_detail(request, order_number):
    """Detalhes do pedido (sessão)"""
    orders = request.session.get('orders', [])
    order = next((o for o in orders if o['order_number'] == order_number), None)
    if not order:
        messages.error(request, 'Pedido não encontrado.')
        return redirect('store:order_history')
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)

def order_history(request):
    """Histórico de pedidos (sessão)"""
    orders = request.session.get('orders', [])
    orders = list(reversed(orders))
    # Estatísticas
    total_orders = len(orders)
    delivered_count = sum(1 for o in orders if o.get('status') == 'entregue')
    total_spent = round(sum(float(o.get('total_price', 0)) for o in orders), 2)
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered_count': delivered_count,
        'total_spent': total_spent,
    }
    return render(request, 'store/order_history.html', context)

# Catálogo em memória e categorias
ALCOHOL_CHOICES = [
    ('vinhos', 'Vinhos'),
    ('cervejas', 'Cervejas'),
    ('destilados', 'Destilados'),
    ('sem_alcool', 'Sem Álcool'),
]

CATEGORIES = [
    {"slug": "vinhos", "name": "Vinhos", "description": "Seleção especial de vinhos."},
    {"slug": "cervejas", "name": "Cervejas", "description": "Diversas marcas e estilos de cervejas."},
    {"slug": "destilados", "name": "Destilados", "description": "Whisky, vodka, gin e mais."},
    {"slug": "sem-alcool", "name": "Sem Álcool", "description": "Bebidas sem teor alcoólico."},
]

PRODUCTS = [
    {
        "id": 1,
        "slug": "vinho-tinto-reserva",
        "name": "Vinho Tinto Reserva",
        "description": "Vinho tinto encorpado com notas de frutas vermelhas.",
        "price": 79.90,
        "volume": "750 ml",
        "alcohol_content": 13.5,
        "stock": 15,
        "featured": True,
        "available": True,
        "alcohol_type": "vinhos",
        "category_slug": "vinhos",
        "category_name": "Vinhos",
        "image_url": "",
        "alcohol_type_display": "Vinhos",
    },
    {
        "id": 2,
        "slug": "cerveja-artesanal-ipa",
        "name": "Cerveja Artesanal IPA",
        "description": "Cerveja IPA com amargor pronunciado e aromas cítricos.",
        "price": 19.90,
        "volume": "500 ml",
        "alcohol_content": 6.2,
        "stock": 30,
        "featured": True,
        "available": True,
        "alcohol_type": "cervejas",
        "category_slug": "cervejas",
        "category_name": "Cervejas",
        "image_url": "",
        "alcohol_type_display": "Cervejas",
    },
    {
        "id": 3,
        "slug": "vodka-premium",
        "name": "Vodka Premium",
        "description": "Vodka destilada cinco vezes para máxima pureza.",
        "price": 89.90,
        "volume": "1 L",
        "alcohol_content": 40.0,
        "stock": 20,
        "featured": False,
        "available": True,
        "alcohol_type": "destilados",
        "category_slug": "destilados",
        "category_name": "Destilados",
        "image_url": "",
        "alcohol_type_display": "Destilados",
    },
    {
        "id": 4,
        "slug": "refrigerante-cola",
        "name": "Refrigerante Cola",
        "description": "Bebida gaseificada sabor cola.",
        "price": 7.50,
        "volume": "350 ml",
        "alcohol_content": None,
        "stock": 100,
        "featured": False,
        "available": True,
        "alcohol_type": "sem_alcool",
        "category_slug": "sem-alcool",
        "category_name": "Sem Álcool",
        "image_url": "",
        "alcohol_type_display": "Sem Álcool",
    },
    {
        "id": 5,
        "slug": "gin-artesanal",
        "name": "Gin Artesanal",
        "description": "Gin com botânicos selecionados.",
        "price": 129.90,
        "volume": "700 ml",
        "alcohol_content": 38.0,
        "stock": 8,
        "featured": True,
        "available": True,
        "alcohol_type": "destilados",
        "category_slug": "destilados",
        "category_name": "Destilados",
        "image_url": "",
        "alcohol_type_display": "Destilados",
    },
    {
        "id": 6,
        "slug": "cerveja-lager",
        "name": "Cerveja Lager",
        "description": "Cerveja leve e refrescante.",
        "price": 12.90,
        "volume": "350 ml",
        "alcohol_content": 4.5,
        "stock": 50,
        "featured": False,
        "available": True,
        "alcohol_type": "cervejas",
        "category_slug": "cervejas",
        "category_name": "Cervejas",
        "image_url": "",
        "alcohol_type_display": "Cervejas",
    },
]

# Helpers de catálogo

def get_category_by_slug(slug):
    for c in CATEGORIES:
        if c["slug"] == slug:
            return c
    return None


def get_product_by_id(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def get_product_by_slug(slug):
    for p in PRODUCTS:
        if p["slug"] == slug and p.get("available", True):
            return p
    return None


def filter_products(category_slug="", alcohol_type="", search_query=""):
    results = [p for p in PRODUCTS if p.get("available", True)]
    if category_slug:
        results = [p for p in results if p["category_slug"] == category_slug]
    if alcohol_type:
        results = [p for p in results if p["alcohol_type"] == alcohol_type]
    if search_query:
        sq = search_query.lower()
        results = [p for p in results if sq in p["name"].lower() or sq in p["description"].lower()]
    # Ordenar: destaque primeiro
    results.sort(key=lambda p: (not p.get("featured", False)),)
    return results

# Helpers de carrinho na sessão

def get_session_cart(request):
    cart = request.session.get("cart", {"items": []})
    # Normalizar estrutura
    cart.setdefault("items", [])
    return cart


def save_session_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def build_cart_context(cart):
    items = []
    total_items = 0
    total_price = 0.0
    for it in cart.get("items", []):
        subtotal = round(float(it["price"]) * int(it["quantity"]), 2)
        total_items += int(it["quantity"])
        total_price += subtotal
        item_view = {
            "product_id": it["product_id"],
            "slug": it["slug"],
            "name": it["name"],
            "description": it.get("description", ""),
            "price": it["price"],
            "quantity": it["quantity"],
            "volume": it.get("volume"),
            "alcohol_type_display": it.get("alcohol_type_display", ""),
            "image_url": it.get("image_url", ""),
            "subtotal": round(subtotal, 2),
        }
        items.append(item_view)
    return {
        "cart_items": items,
        "cart_total_items": total_items,
        "cart_total": round(total_price, 2),
    }
