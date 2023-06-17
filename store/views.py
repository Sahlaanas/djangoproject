from django.shortcuts import render, redirect
from user_category.models import Category
from user_brand.models import Brand
from django.db.models import F
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Product,screenSizeVariant,ProductAttribute
from django.contrib import messages
from django.db.models import Min, Max
from django.http import JsonResponse




# Create your views here.
def store(request):
    
    # products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
#     filter_prices = price_filter.objects.all()
    product = Product.objects.all()
    
    product_count = product.count()
    Cat_id = request.GET.get('categories')
#     filter_price_id = request.GET.get('filter_price')
    brand_id = request.GET.get('brand')
    sort = request.GET.get('sort')
    search_query = request.GET.get('search_query')
    minMaxPrice = ProductAttribute.objects.aggregate(Min('price'), Max('price'))
    

    
    
    
    if search_query:
        product = Product.objects.filter(product_name__icontains=search_query)
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        


    elif Cat_id:
        product = Product.objects.filter(category__id=Cat_id)
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
#     elif filter_price_id:
#         product = Product.objects.filter(filt_price=filter_price_id)
#         paginator = Paginator(product, 3)
#         page = request.GET.get('page')
#         paged_product = paginator.get_page(page)
#         p_count = product.count()
        
    elif brand_id:
        product = Product.objects.filter(brand__id=brand_id)
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif sort == 'atoz':
        product = Product.objects.order_by('product_name')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
        
    elif sort == 'ztoa':
        product = Product.objects.order_by('-product_name')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif sort == 'ltoh':
        product = Product.objects.order_by('price')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif sort == 'htol':
        product = Product.objects.order_by(F('price').desc())
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
               
    else:
        product = Product.objects.all()
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        

        
    context = {
        # 'products' : products,
        'categories' : categories,
        'brands' : brands,
      #   'filter_prices' : filter_prices,
        'product' : paged_product,
        'product_count' : product_count,
        'search_query': search_query,
        'p_count' : p_count,
        'minMaxPrice' : minMaxPrice,
       
    }
    for category in categories:
        product_count = category.product_set.count()
        category.product_count = product_count
    
    return render(request, 'store/store.html', context)

def productview(request, cat_slug, prod_slug):
    if Category.objects.filter(slug=cat_slug).exists():
        if Product.objects.filter(slug=prod_slug).exists():
            product = Product.objects.filter(slug=prod_slug).first()
            related_product = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
            size = ProductAttribute.objects.filter(product=product).values('size__id','size__size_name','price','ram__id').distinct()
            ram = ProductAttribute.objects.filter(product=product).values('ram__id','ram__RAM_name').distinct()
            productattr = ProductAttribute.objects.filter(product__slug=prod_slug).first()
            if productattr.offer:
                price=productattr.get_offer()
                print(price,"==============price1")
            else:
                price=productattr.price
                print(price,"==============price2")
            
            
            
            
            context = {
                'product' : product,
                'related_product' : related_product,
                'size' : size,
                'ram' : ram,
                'price': price,
                'productattr' : productattr
                
                
            }
            
           

        else:
            messages.error(request, "No such products found") 
            return redirect('store')
    else:
        messages.error(request, "No such category found")
        return redirect('store')
    return render(request, 'store/productview.html', context)


