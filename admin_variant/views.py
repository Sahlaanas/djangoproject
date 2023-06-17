from django.shortcuts import render, redirect
from user_home.models import Banner
from django.contrib import messages
from user_category.models import Category
from store.models import Product,ProductAttribute,screenSizeVariant,RAMVariant,Offer

# Create your views here.
def variantlist(request):
      query = request.GET.get('query')
      if query:
            variant = ProductAttribute.objects.filter(product__product_name__icontains=query)
      else:
            variant = ProductAttribute.objects.all()
      category = Category.objects.all()
      product = Product.objects.all()
      size = screenSizeVariant.objects.all()
      ram = RAMVariant.objects.all()
      offer = Offer.objects.all()
      context = {
            'variant' : variant,
            'category' : category,
            'product' : product,
            'size' : size,
            'ram' : ram,
            'offer' : offer
            
      }
      return render(request, 'dashboard/variantlist.html', context)

def addvariant(request):
      if request.method == 'POST':
          product_id = request.POST['product']
          size_id = request.POST['size']
          ram_id = request.POST['ram']
          stock = request.POST['stock']
          offer_id = request.POST['offer']
          price = request.POST['price']
          image = request.FILES.get('image', None)
        
        # Validation
       
          if product_id == '' or size_id == '' or ram_id =='' or stock =='' or price =='':
               messages.error(request, "Some fields are empty")
               return redirect('variantlist')
          if not image:
               messages.error(request, "Image not uploaded")
               return redirect('variantlist')
      
          product = Product.objects.get(id=product_id)
          size = screenSizeVariant.objects.get(id=size_id)
          ram = RAMVariant.objects.get(id=ram_id)
          
        
        # Save the brand
          
          new_variant = ProductAttribute.objects.create(
                product=product,
                size=size,
                ram=ram,
                stock=stock,
                price=price,
                image=image
                
                
                
            
        )
          messages.success(request, 'Variant added successfully')
          return redirect('variantlist')
        
      return render(request, 'dashboard/variantlist.html',new_variant)



def editvariant(request,editvariant_id):
    if request.method == 'POST':
          product_id = request.POST['product']
          size_id = request.POST['size']
          ram_id = request.POST['ram']
          stock = request.POST['stock']
          offer_id = request.POST['offer']
          price = request.POST['price']
          image = request.FILES.get('image', None)
        
# validation
     

          if product_id == ''  or size_id == '' or ram_id ==''or stock ==''or offer_id ==''or price =='':
              messages.error(request, "Some field are empty")
              return redirect('variantlist')
          try:
             variant = ProductAttribute()
             eimage = request.FILES.get('image')
             if eimage:
                variant.image = image
                variant.save()
          except ProductAttribute.DoesNotExist:
             messages.error(request, "Image not found")
             return redirect('variantlist')
        
        # Save
        
          product = Product.objects.get(id=product_id)
          ram = RAMVariant.objects.get(id=ram_id)
          size = screenSizeVariant.objects.get(id=size_id)
          offer = Offer.objects.get(id=offer_id)
          variant = ProductAttribute.objects.get(id=editvariant_id)
          variant.product = product
          variant.offer = offer
          variant.ram = ram
          variant.size = size
          variant.price = price
          variant.stock = stock
          
          
        
          variant.save()
          return redirect('variantlist')
    
def deletevariant(request,deletevariant_id):
    variant = ProductAttribute.objects.get(id=deletevariant_id)
    variant.delete()
    return redirect('variantlist')
