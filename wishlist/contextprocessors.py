from .models import Wishlist

def wishlist_counter(request):
    if request.user.is_authenticated:
        counter = Wishlist.objects.filter(user=request.user).count()
    else:
        counter = 0
    
    return {'wishlist_counter': counter}
