def cart_context(request):
    """Context processor: fornece contagem de itens do carrinho a partir da sessão"""
    cart = request.session.get('cart', {'items': []})
    cart_items_count = 0
    for it in cart.get('items', []):
        try:
            cart_items_count += int(it.get('quantity', 1))
        except (TypeError, ValueError):
            cart_items_count += 1
    return {
        'cart_items_count': cart_items_count,
    }
