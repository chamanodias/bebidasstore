from .models import Cart, CartItem

def cart_context(request):
    """Context processor para disponibilizar informações do carrinho em todos os templates"""
    cart = None
    cart_items_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items_count = cart.get_total_items()
        except Cart.DoesNotExist:
            cart_items_count = 0
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_items_count = cart.get_total_items()
            except Cart.DoesNotExist:
                cart_items_count = 0
    
    return {
        'cart': cart,
        'cart_items_count': cart_items_count,
    }
