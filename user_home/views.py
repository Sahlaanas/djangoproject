from django.shortcuts import render, redirect
from useraccount.models import Account
from user_category.models import Category
from user_brand.models import Brand
from user_home.models import Banner
from store.models import Product
from django.contrib import messages
 

# Create your views here.

def home(request):
    user = Account.objects.all()
    catogories = Category.objects.all()
    brands = Brand.objects.all()
    banners = Banner.objects.all()
    products = Product.objects.all()
    
    
    context = {
        'user': user,
        'brands' : brands,
        'banners' : banners,
        'categories' : catogories,
        'products' : products,
        
    }
    
    return render(request, 'user_home/index.html', context)

def storeview(request,slug):
    if(Category.objects.filter(slug=slug)):
        product = Product.objects.filter(category__slug = slug)
        category_name = Category.objects.filter(slug=slug).first()
        context = {
            'product' : product,
            'category_name' : category_name,
            
        }
        return render(request, 'store/store.html', context)
    else:
        messages.warning(request, "No such category found")
        return redirect('home')
    
    
def searchproduct(request):
    if request.method == 'POST':
        searched = request.POST.get('productsearch')
        if searched == "":
            messages.warning(request, "search something")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(product_name__icontains=searched).first()
            if product:
                return redirect('/store/store/'+product.category.slug+'/'+str(product.slug))
            else:
                messages.error(request, "Search not found")
                return redirect(request.META.get('HTTP_REFERER'))
                   
    return redirect(request.META.get('HTTP_REFERER'))


def bookservice(request):
    return render(request, 'user_home/404.html')