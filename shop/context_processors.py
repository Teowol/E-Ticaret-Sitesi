def cart_counter(request):
    cart = request.session.get('cart', {})
    total_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return {'cart_total_count': total_count}