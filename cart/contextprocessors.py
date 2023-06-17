from .models import CartItem
def cart_counter(request):
    if request.user.is_authenticated:
        counter = CartItem.objects.filter(cart__is_paid=False, cart__user=request.user).count()
    else:
        counter = 0
    
    return {'cart_counter': counter}
