from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from checkout.models import Order,Order_item
from django.shortcuts import render, get_object_or_404
from store.models import Product
from order.models import Wallet


# Create your views here.
def myOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {}
    if orders:
        context = {
            'orders': orders
        }
    return render(request, 'checkout/placeOrder.html', context)



def orderview(request, t_no):
      order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
      orderitems = Order_item.objects.filter(order=order)
      context = {
            'order' : order,
            'orderitems' : orderitems,
      }
      
      return render(request, 'checkout/orderview.html', context)





def user_order_track(request, id):
    order_item = get_object_or_404(Order_item, id=id)
    
    orderstatus = [
        (Order_item.ORDER_STATUS_CHOICES.index(choice) + 1, choice[1]) for choice in Order_item.ORDER_STATUS_CHOICES
    ]
      
    statusIndex = {
        'pending': 1,
        'processing': 2,
        'out for shipping': 3,
        'shipped': 4,
        'delivered': 5,
        'cancelled': 6,
        'refunded': 7,
    }

    trackIndex = 0
    for value, idx in statusIndex.items():
        if value.lower() == order_item.status.lower():
            trackIndex = idx 
            break
    
    context = {
        'order_item': order_item,
        'orderstatus': orderstatus,
        'trackIndex': trackIndex
    }
    
    return render(request, "checkout/trackorder.html", context)





# Order Cancel
from django.http import HttpResponseBadRequest
def ordercancel(request):
    orderid = request.POST.get('order_id')
    orderitem_id = request.POST.get('orderitem_id')
    # Check if orderitem_id is valid
    if not orderitem_id:
        return HttpResponseBadRequest("Invalid orderitem_id")

    try:
        orderitem_id = int(orderitem_id)
    except ValueError:
        return HttpResponseBadRequest("Invalid orderitem_id")

    orderitem = Order_item.objects.filter(id=orderitem_id).first()

    if not orderitem:
        return HttpResponseBadRequest("Order item not found")

    order = Order.objects.filter(id=orderid).first()
    qty = orderitem.quantity
    pid = orderitem.product.id
    product = Product.objects.filter(id=pid)
    
    
    if order.payment_mode.method == 'Razorpay':
        order = Order.objects.get(id=orderid)
        total_price = order.total_price
        try:
            wallet = Wallet.objects.get(user=request.user)
            wallet.wallet += total_price
            wallet.save()
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user, wallet=total_price)
       
       


    orderitem.quantity = 0
    orderitem.status = 'Cancelled'
    orderitem.save()
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
