from store.models import Brand
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user_category.models import Category
from useraccount.models import Account
from store.models import Product
from django.http import JsonResponse


def brandlist(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    query = request.GET.get('query')
    if query:
        Brands = Brand.objects.filter(brand_name__icontains=query)
    else:
        Brands = Brand.objects.all()
        
    context = {
        'Brands' : Brands
    }
    
    
    return render(request, 'dashboard/brandlist.html', context )

def createbrand(request):
    if request.method == 'POST':
        name = request.POST['brand_name']
        brand_description = request.POST['brand_description']
        brand_address = request.POST['brand_address']
        image = request.FILES.get('image', None)
        
        # Validation
        if Brand.objects.filter(brand_name=name).exists():
            messages.error(request, 'Brand name already exists')
            return redirect('brandlist')
        if name == '' or brand_address == '':
            messages.error(request, "Name  field is empty")
            return redirect('brandlist')
        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('brandlist')

        
        # Save the brand
        new_brand = Brand.objects.create(
            brand_name=name,
            brand_description=brand_description,
            brand_image=image,
            brand_address=brand_address,
        )
        messages.success(request, 'Brand added successfully')
        return redirect('brandlist')
        
    return render(request, 'dashboard/brandlist.html',new_brand)

def editbrand(request,editbrand_slug):
    if request.method == 'POST':
        name = request.POST['brand_name']
        brand_description = request.POST['brand_description']
        brand_address = request.POST['brand_address']
        
# validation
     

        if name == ''  or brand_address == '':
            messages.error(request, "Name and address field are empty")
            return redirect('brandlist')
        try:
            Brands = Brand.objects.get(slug=editbrand_slug)
            eimage = request.FILES.get('image')
            if eimage:
                Brands.cat_image = eimage
                Brands.save()
        except Brand.DoesNotExist:
            messages.error(request, "Image not found")
            return redirect('brandlist')
        
        # Save
        
# Save       
        Brands = Brand.objects.get(slug=editbrand_slug)
        Brands.brand_name = name
        Brands.brand_description = brand_description
        Brands.brand_address = brand_address
        
        Brands.save()
        return redirect('brandlist')
    
def deletebrand(request,deletebrand_slug):
    Brands = Brand.objects.get(slug=deletebrand_slug)
    Brands.delete()
    return redirect('brandlist')


#=====================CATEGORY==============================


def categorylist(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    query = request.GET.get('query')
    if query:
        categories = Category.objects.filter(category_name__icontains=query)

    else:
    
        categories = Category.objects.all()
        
    context = {
        'categories' : categories
    }
    

   
    return render(request, 'dashboard/categorylist.html',context)

def createcategory(request):
    if request.method == 'POST':
        name = request.POST['category_name']
        cat_description = request.POST['category_description']
        image = request.FILES.get('image', None)
        
        # Validation
        if Category.objects.filter(category_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('categorylist')
        if name == '' :
            messages.error(request, "Name  field is empty")
            return redirect('categorylist')
        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('categorylist')

        
        # Save the product
        new_category = Category.objects.create(
            category_name=name,
            description=cat_description,
            cat_image=image,
        )
        messages.success(request, 'Category added successfully')
        return redirect('categorylist')

        
    
    return render(request, 'dashboard/categorylist.html',new_category)


def editcategory(request,editcategory_slug):
    if request.method == 'POST':
        name = request.POST['category_name']
        cat_description = request.POST['category_description']
        
# validation
     

        if name == ''  or cat_description == '':
            messages.error(request, "Name and description field are empty")
            return redirect('categorylist')
        try:
            cat = Category.objects.get(slug=editcategory_slug)
            eimage = request.FILES.get('image')
            if eimage:
                cat.cat_image = eimage
                cat.save()
        except Category.DoesNotExist:
            messages.error(request, "Image not found")
            return redirect('categorylist')
        
        # Save
        
# Save       
        cat = Category.objects.get(slug=editcategory_slug)
        cat.category_name = name
        cat.description = cat_description
        
        cat.save()
        return redirect('categorylist')
    
def deletecategory(request,deletecategory_slug):
    cat = Category.objects.get(slug=deletecategory_slug)
    cat.delete()
    messages.info(request,f'deleted category {cat.category_name}')
    return redirect('categorylist')

def userlist(request):
    query = request.GET.get('query')
    if query:
        userdetails = Account.objects.filter(username__icontains=query)

    else:
        userdetails = Account.objects.all().order_by('id')
    context = {
        'userdetails' : userdetails
    }
    return render(request, 'dashboard/userlist.html', context)


def blockUnblock(request, id):

    user=get_object_or_404(Account,id=id)
    if user.is_superuser:
        messages.error(request,"Admin block is not allowed")
        return redirect(userlist)
        
        
    
    if user == request.user:
        messages.error(request,"Self block is not allowed")
        return redirect(userlist)
    else:
        

        if user.is_active:

            user.is_active=False

            user.save()

            return redirect(userlist)
        
        else:

            user.is_active=True

            user.save()

            return redirect(userlist)
        
    




    
    