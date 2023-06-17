from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models.functions import TruncDay, Cast
from checkout.models import Order_item
from django.db.models import Sum, DateField
from checkout.models import Order
from useraccount.models import Account
from django.views.decorators.cache import cache_control


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def admin_login(request):
    if request.user.is_superuser:
        return redirect(admin_home)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect(admin_home)
            else:
                messages.error(request,f"{user} is not have admin access")
                return redirect(admin_login)
        else:
            messages.info(request,'credential mismatch')
            return redirect(admin_login)
    else:
        return render(request,'admin_account/login.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@login_required(login_url='admin_login')   
def admin_home(request):
    if not request.user.is_superuser:
        return redirect(admin_login)

    delivered_item = Order_item.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_item:
        revenue+=item.order.total_price

    top_selling = Order_item.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = Order_item.objects.all().order_by('-id')[:5]


    # Getting the current date
    today = datetime.today()
    date_range = 7

    # Get the date 7 days ago
    four_days_ago = today - timedelta(days=date_range)

    #filter orders based on the date range
    orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)

    # Getting the sales amount per day
    sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')

    # Getting the dates which sales happpened
    sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':Account.objects.count(),
        'sales':Order_item.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
        'sales_dates' : sales_dates
    }
    
    return render(request,'dashboard/index.html',context)



@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def admin_logout(request):
    logout(request)
    return redirect(admin_login)


def admin_sales(request):
    if not request.user.is_superuser:
        return redirect(admin_login)
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(admin_sales)
        
        if start_date ==  end_date :
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = Order_item.objects.filter(order__created_at__date=date_obj.date())
            if order_items:
                context.update(sales = order_items,s_date=start_date,e_date = end_date)
                return render(request,'dashboard/admin_sales.html',context)
            else:
                messages.error(request,'no data found')
            return redirect(admin_sales)

        order_items = Order_item.objects.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)

        if order_items:
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')

    return render(request,'dashboard/admin_sales.html',context)