from django.shortcuts import render, redirect
from checkout.models import Order_item, Order
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def orderlist(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    query = request.GET.get('query')
    if query:
        orders = Order.objects.filter(tracking_no__contains=query)
    else:
        orders = Order.objects.all().order_by('id')
    
    orderitems = Order_item.objects.filter(order__in=orders)

  
    context = {
        'orderitems': orderitems,
        'orders': orders
    }
    return render(request, 'dashboard/orderlist.html', context)




@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemId')
        selected_value = request.POST.get('selectedValue')
       

        try:
            order_item = Order_item.objects.get(pk=item_id)
            order_item.status = selected_value
            order_item.save()

            return JsonResponse({'success': True, 'status_display': order_item.get_status_display()})
        except Order_item.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


