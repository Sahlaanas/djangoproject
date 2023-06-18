from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from store.models import Product,ProductAttribute
from cart.models import CartItem,Cart
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def add_to_cart(request):
     
      if request.user.is_authenticated:     
            user = request.user
            cart,_ = Cart.objects.get_or_create(user=user, is_paid=False)
            
            # Retrieve data from request.GET
            product_id = request.GET.get('id')
            image = request.GET.get('image')
            title = request.GET.get('title')
            qty = int(request.GET.get('qty'))
            price = float(request.GET.get('price'))
            print(product_id,image,title,qty,price)
            
            # Find the product and variant
            variant=ProductAttribute.objects.get(price=price)
            product = get_object_or_404(Product, id=product_id)
           
            
            # Create or update the cart item
            cart_items = CartItem.objects.filter(cart=cart, product=product, variant=variant)

            if cart_items.exists():
            # Choose one of the cart items and update it
                  cart_item = cart_items.first()
                  cart_item.product_quantity += int(request.GET['qty'])
                  cart_item.save()
            else:
                  
            # Create a new cart item
                  cart_item = CartItem.objects.create(
                        cart=cart, product=product, variant=variant,
                        product_quantity=int(request.GET['qty'])
                  )

            
            # Retrieve the session cart items
            
            if 'cartdata' in request.session:
                  print("it is working......")
                  cart_data=request.session['cartdata']
                  
            
            # Associate session cart items with the user's cart
                  for prod_id, item_data in cart_data.items():
                        session_qty = int(item_data['qty'])
                        session_price = int(item_data['price'])
                        variant_st=ProductAttribute.objects.get(price=session_price)
                                                
                        if session_qty > 0:
                              cart_items = CartItem.objects.filter(cart=cart, product=product, variant=variant)

                              if cart_items.exists():
            # Choose one of the cart items and update it
                                    cart_item = cart_items.first()
                                    cart_item.product_quantity += int(request.GET['qty'])
                                    cart_item.save()
                              else:
                  
            # Create a new cart item
                                    cart_item = CartItem.objects.create(
                                          cart=cart, product=product, variant=variant,
                                          product_quantity=int(request.GET['qty'])
                                    )
                  
            # Clear the session cart data
                  del request.session['cartdata']
            
            # Return response
            print('cartcount',cart_items.count())
            return JsonResponse({'status': 'Item added to cart', 'total_items': cart_items.count()})
            
      else:
            
            cart_p={}
            cart_p[str(request.GET['id'])]={
                  'image':request.GET['image'],
                  'title':request.GET['title'],
                  'qty':request.GET['qty'],
                  'price':request.GET['price']
                  
            }
            price=request.GET['price']
            variant=ProductAttribute.objects.get(price=price)      
            cart_p[str(request.GET['id'])]['variant']=variant.id
            
            if 'cartdata' in request.session:
                  cart_data=request.session['cartdata']
                  
                  
                  if str(cart_p[str(request.GET['id'])]['variant']) in str(cart_data[str(request.GET['id'])]['variant']):
                        cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
                        cart_data.update(cart_data)
                        request.session['cartdata']=cart_data
                  else:
    
                        cart_data.update(cart_p)
                        request.session['cartdata']=cart_data
            else:
                  request.session['cartdata']=cart_p
            return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'status':"Item added Successfully"})



def cart(request):
      if request.user.is_authenticated:
            cart = Cart.objects.filter(is_paid = False, user = request.user)
            cartitem = CartItem.objects.filter(cart__is_paid = False, cart__user = request.user)
            
            tax = 0
            subtotal = 0
            grandtotal = 0
            
            
            for item in cartitem:
                   if item.variant.offer:
                        subtotal += item.product_quantity*item.variant.get_offer()
                   else:
                        subtotal += item.product_quantity*item.variant.price
                  
            tax=round(subtotal*0.18)
            grandtotal = subtotal+tax+70
            
            context = {
                  'cart' : cart,
                  'cartitem' : cartitem,  
                  'subtotal' : subtotal, 
                  'tax' : tax, 
                  'grandtotal' : grandtotal,
            }
            return render(request, 'cart/cart.html',context)
      else:
            if 'cartdata' in request.session:
            
                  total_amt = 0
                  for p_id,item in request.session['cartdata'].items():
                        total_amt+=int(item['qty'])*float(item['price'])
                        
                  context={
                        'cart_data':request.session['cartdata'],
                        'totalitems' : len(request.session['cartdata']),
                        'total_amt' : total_amt
                        
                        
                        
                  }
            
                  
                  return render(request, 'cart/cart2.html',context)
            else:
                  messages.error(request,"Cart is empty")
                  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteCartItem(request):
      if request.user.is_authenticated:
            p_id=request.GET['item_id']
            if p_id is not None:

                  cart_items = CartItem.objects.filter(cart__user=request.user, id=p_id)
                  if cart_items.exists():
                        cart_items.delete()
                        return JsonResponse({'status':"Deleted Succesfully"})

      
      else:
            
            p_id=str(request.GET['product_id'])
            print(p_id)
            if 'cartdata' in request.session:
                  if p_id in request.session['cartdata']:
                        cart_data=request.session['cartdata']
                        s= request.session['cartdata'][p_id]
                        s.delete()
                        request.session['cartdata']=cart_data
                        
            total_amt=0
            for p_id,item in request.session['cartdata'].items():
                  total_amt+=int(item['qty'])*float(item['price'])
                  
            context={
                  'cart_data':request.session['cartdata'],
                  'totalitems' : len(request.session['cartdata']),
                  'total_amt' : total_amt
                  
                  
                  
            }
            data=render_to_string('cart/cart2.html',context)
            return JsonResponse({'data':data,'status':"Deleted Succesfully"})

def updateCartItem(request):
      if request.user.is_authenticated:
            item_id = int(request.GET.get('item_id'))
           
            try:
                  cart = CartItem.objects.get(id=item_id, cart__user=request.user)
                  item_qty = int(request.GET.get('item_qty'))
                  cart.product_quantity = item_qty
                  cart.save()
                  
                  
                  
                  
                  context={
                        'status': "Updated Successfully",
                        
                        'quantity': cart.product_quantity,
                        
                        }
            except ObjectDoesNotExist:
                  pass
            data=render_to_string('cart/cart.html',context)
            return JsonResponse({'data':data,'status':"Updated Succesfully"})
        
      
      else:
            
            p_id=str(request.GET['product_id'])
            qty=request.GET['product_qty']
            print(p_id,"===============",qty)
            if 'cartdata' in request.session:
                  if p_id in request.session['cartdata']:
                        cart_data=request.session['cartdata']
                        cart_data[str(request.GET['product_id'])]['qty']=qty
                        request.session['cartdata']=cart_data
                        
            total_amt=0
            for p_id,item in request.session['cartdata'].items():
                  total_amt+=int(item['qty'])*float(item['price'])
                  
            context={
                  'cart_data':request.session['cartdata'],
                  'totalitems' : len(request.session['cartdata']),
                  'total_amt' : total_amt
                  
                  
                  
            }
            data=render_to_string('cart/cart2.html',context)
            return JsonResponse({'data':data,'status':"Updated Succesfully"})


  
        


