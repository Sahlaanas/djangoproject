from django.shortcuts import render, redirect
from store.models import Product, Brand, Product_Image, screenSizeVariant
from user_category.models import Category
from django.contrib import messages
from cart.models import Coupon


# Create your views here.
def productlist(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        
        products = Product.objects.all().order_by('id')
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    variants = screenSizeVariant.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'variants' : variants
    }
    return render(request ,'dashboard/productlist.html',context)


def createproduct(request):
    
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        description = request.POST['product_description']
        brand_name = request.POST.get('brand')
        category_id = request.POST.get('category')

        
        try:
            image=request.FILES['image']
            multiple_images = request.FILES.getlist('multiple_images')
        except:
            messages.error(request, 'Add product image')
            return redirect('productlist')
        
   
            
        

        # Validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('productlist')
        if name == '' or price == '':
            messages.error(request, "Name or Price field is empty")
            return redirect('productlist')
        
        categorys = Category.objects.get(id=category_id) 
        Brands = Brand.objects.get(brand_name=brand_name)
        

        # Save the product
        new_product = Product.objects.create(
            product_name=name,
            price=price,
            product_description=description,
            brand=Brands,
            category=categorys,
           
            
            
        )
        new_product.save()
        if multiple_images:
            
            for image in multiple_images:
                image_model=Product_Image(product=new_product,image=image)
                image_model.save()

        
        if image:
            product_image = Product_Image.objects.create(
                product=new_product,
                image=image,
            )
            product_image.save()
        else:
            messages.error(request, 'Add product image')
            return redirect('productlist')
            

        messages.success(request, 'Product added successfully')
        return redirect('productlist')

    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'categories': categories,
        'brands': brands,
        'new_product':new_product
    }
    return render(request, 'dashboard/productlist.html', context)

def deleteproduct(request,prod_slug):
    pro = Product.objects.get(slug=prod_slug)
    pro.delete()
    return redirect('productlist')

def editproduct(request, prod_slug):
    if request.method == 'POST':
        pname = request.POST['product_name']
        pprice = request.POST['product_price']
        description = request.POST['product_description']
        brandname = request.POST.get('brand')
        category_id = request.POST.get('category')
        variant = request.POST.get('variant')

        # Validation
        if pname == '' or pprice == '':
            messages.error(request, "Name or Price field is empty")
            return redirect('productlist')

        try:
            product = Product.objects.get(slug=prod_slug)
            images = product.product_image_set.all()
            if images:
                for i, image in enumerate(images):
                    eimage = request.FILES.get(f'image{i+1}')
                    if eimage:
                        image.image = eimage
                        image.save()
        except Product.DoesNotExist:
            messages.error(request, "Product not found")
            return redirect('productlist')

        # Save
        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(brand_name=brandname)

        product.product_name = pname
        product.price = pprice
        product.product_description = description
        product.brand = brand
        product.category = category

        product.save()

        return redirect('productlist')
    
def couponlist(request):
    query = request.GET.get('query')
    if query:
        coupon = Coupon.objects.filter(coupon_code__icontains=query)
    else:
        coupon = Coupon.objects.all()
    context = {
        'coupon' : coupon
    }
    return render(request, 'dashboard/coupon.html', context)



def addcoupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount_price = request.POST.get('discount_price')
        minimum_amount = request.POST.get('minimum_amount')
        
        if coupon_code == '' or discount_price == '' or minimum_amount == '':
            messages.error(request, "Some  fields are empty")
            return redirect('couponlist')

        
        try:
            is_expire = request.POST.get('is_expired', False)
            is_apply = request.POST.get('is_applied', False)

            
            if is_expire == 'on':
                is_expire = True
            else:
                is_expire = False
            if is_apply == 'on':
                is_apply = True
            else:
                is_apply=False
        except:
            is_expire = False
            is_apply=False


 
        
        # Create a new Coupon object
        coupon = Coupon(
            coupon_code=coupon_code,
            discount_price=discount_price,
            minimum_amount=minimum_amount,
            is_expired=is_expire,
            is_applied=is_apply
           
        )
        coupon.save()        
        return redirect('couponlist')
    
def deletecoupon(request,deletecoupon_id):
    code = Coupon.objects.get(id=deletecoupon_id)
    code.delete()
    return redirect('couponlist')


def editcoupon(request, editcoupon_id):
     if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount_price = request.POST.get('discount_price')
        minimum_amount = request.POST.get('minimum_amount')

        # Validation
        if coupon_code == '' or discount_price == '' or minimum_amount == '':
            messages.error(request, "Some  fields are empty")
            return redirect('couponlist')

        try:
            is_expire = request.POST.get('is_expired', False)
            is_apply = request.POST.get('is_applied', False)

            
            if is_expire == 'on':
                is_expire = True
            else:
                is_expire = False
            if is_apply == 'on':
                is_apply = True
            else:
                is_apply=False
        except:
            is_expire = False
            is_apply=False

        # Save
        coupon = Coupon.objects.get(id=editcoupon_id)

        coupon.coupon_code = coupon_code
        coupon.discount_price = discount_price
        coupon.minimum_amount = minimum_amount
        coupon.is_applied = is_apply
        coupon.is_expired = is_expire
       
        coupon.save()

        return redirect('couponlist')

    

