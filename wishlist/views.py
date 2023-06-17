from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . models import Wishlist
from django.http import JsonResponse
from store.models import Product,ProductAttribute
from wishlist.models import Wishlist
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
def wishlist(request):
    wishlistitems = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlistitems' : wishlistitems,
        }
    return render(request, 'wishlist/wishlist.html', context)






def addTowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            price = int(request.POST.get('price'))
            product_check = Product.objects.get(id=prod_id)
            variant=ProductAttribute.objects.filter(price=price)
            
           
            
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status' : "Product already in wishlist"})
                else:
                    variants = ProductAttribute.objects.filter(price=price)
                    if variants.exists():
                        variant = variants.first()  # Choose the first object from the queryset
                        Wishlist.objects.create(user=request.user, product_id=prod_id, variant=variant)
                        return JsonResponse({'status' : "Product added to wishlist"})
                    else:
                        return JsonResponse({'status' : "No such product variant found"})

            else:
                return JsonResponse({'status' : "No such product found"})
        else:
            return JsonResponse({'status' : "Login to continue"})
    return redirect('/')            
   
   
def remove_wishlist(request):
    if request.method == "POST":
        prod_id = request.POST.get('product_id')
        print(prod_id)
        
        if prod_id is not None:
            prod_id = int(prod_id)
            if Wishlist.objects.filter(product_id=prod_id).exists():
                wishitem = Wishlist.objects.get(product_id=prod_id)
                wishitem.delete()
                messages.success(request, "Item deleted successfully")
    return redirect('wishlist')
            
        
