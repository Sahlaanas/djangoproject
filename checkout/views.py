from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from coupon.models import Coupon,Usercoupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from useraccount.models import Account
from user_profile.models import User_Address
from . models import Order, Order_item, Payment_methods
from store.models import Product
import random
from django.http import JsonResponse,HttpResponseRedirect

from django.views.decorators.cache import cache_control
from order.models import Wallet




# Create your views here.

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def checkout(request):
    rawcart = CartItem.objects.filter(cart__user=request.user)
    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
    carts = Cart.objects.filter(user=request.user)
    
    # Remove cart items where product_quantity exceeds size_variant stock
    coupon_code = request.POST.get('coupon_code')

    address = User_Address.objects.filter(user=request.user)
    cartitems = CartItem.objects.filter(cart__user=request.user)
    tax = 0
    subtotal = 0
    grandtotal = 0
    
    
    
    
    for item in cartitems:
        if item.variant.offer:
            subtotal += item.product_quantity*item.variant.get_offer()
        else:
            subtotal += item.product_quantity*item.variant.price
        
    tax = round(subtotal * 0.18)
    
    grandtotal = subtotal + 70 + tax
   
    
    usercoupon = Usercoupon.objects.filter(user=request.user).last()
    coupons = Coupon.objects.all()
        
        
    userprofile = User_Address.objects.filter(user=request.user).first()
   
 
    
    
    context = {
        'cartitems': cartitems,
        'subtotal': subtotal,
        'grandtotal': grandtotal,
        'tax' : tax,
        'usercoupon' : usercoupon,
        'userprofile' : userprofile,
        'cart' : cart_obj,
        'carts' : carts,
        'coupons' : coupons,
        'address' : address
        
    }
    
    return render(request, 'checkout/checkout.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def placeorder(request):
    if request.method == "POST":
        currentuser = Account.objects.filter(id=request.user.id).first()
        payment_mode_value = request.POST.get('payment_mode')
        payment_mod = Payment_methods.objects.get(method__icontains=payment_mode_value)
        # userprofile = User_Address.objects.filter(user=request.user).first()
        address_id=request.POST.get('address')
        

        if address_id is None:
            messages.error(request,"Address field are mandatory")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        neworder = Order()
        address = User_Address.objects.get(id=address_id)
        neworder.user_address = address
        neworder.user = request.user
        neworder.payment_mode = payment_mod
        neworder.payment_id = request.POST.get('payment_id')
        
  
        
        

        cartitems = CartItem.objects.filter(cart__user=request.user)
        cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
        tax = 0
        subtotal = 0
        grandtotal = 0

        for item in cartitems:
            subtotal += item.product_quantity*item.variant.price

        tax = subtotal * 0.18

        grandtotal = subtotal + tax + 50
        
        if (payment_mod.method == "Wallet"):
            try:
                wallet = Wallet.objects.get(user=request.user)
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user, wallet=0)
            
            if wallet.wallet >= grandtotal:
                wallet.wallet = wallet.wallet-grandtotal
                wallet.save()
            else:
                messages.error(request,'Your wallet amount is very low')
                return redirect('checkout')
            
        if Usercoupon.objects.filter(user = request.user).exists():
            usercoupon = Usercoupon.objects.get(user = request.user)
            neworder.total_price = usercoupon.total_price
            usercoupon.delete()
        else:
            neworder.total_price = grandtotal
        
        

        if cart_obj:
            trackno = 'LapK' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno) is None:
                trackno = 'LapK' + str(random.randint(1111111, 9999999))

            neworder.tracking_no = trackno
            neworder.save()

            neworderitems = CartItem.objects.filter(cart__user=request.user)

            for item in neworderitems:
                Order_item.objects.create(
                    user=request.user,
                    order=neworder,
                    product=item.product,
                    price=item.variant.price,
                    quantity=item.product_quantity,
                    total=grandtotal,
                    image=item.variant.image,
                    variant=item.variant
                )

                item.variant.stock -= item.product_quantity
                item.save()

            # To clear cart
            Cart.objects.filter(user=request.user).delete()
            
          

            payMode = request.POST.get('payment_mode')
            if payMode == "Razorpay":
                return JsonResponse({'status': "Your order has been placed"})
            else:
                messages.success(request, "Your order has been placed successfully")

    return render(request, 'checkout/checkout.html')



def razorpaycheck(request):
    cart = CartItem.objects.filter(cart__user=request.user)
    cart_obj = Cart.objects.get(is_paid = False, user=request.user)
    tax = 0
    subtotal = 0
    grandtotal = 0
    
    for item in cart:
        subtotal += item.product_quantity*item.variant.price
        
    tax = subtotal * 0.18
    grandtotal=subtotal + tax + 70


            
    return JsonResponse({
        'total_price' : grandtotal
    })
    
    
