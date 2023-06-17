from django.shortcuts import render, redirect
from store.models import Offer
from django.contrib import messages

# Create your views here.
def offerlist(request):
      query = request.GET.get('query')
      if query:
            offer = Offer.objects.filter(offer_name__icontains=query)
      else:
            offer = Offer.objects.all()
      
      context = {
            'offer': offer
      }
      
      return render(request, 'dashboard/offerlist.html', context)

def addoffer(request):
    if request.method == 'POST':
        offer_name = request.POST['offer_name']
        discount_price = request.POST['discount_amount']
       
        # Validation
        if offer_name == '' or discount_price == '':
            messages.error(request, "Some fields are empty")
            return redirect('offerlist')
        try:
            discount_price = int(discount_price)
            if discount_price < 1:
                messages.error(request, "Price should be a positive number")
                return redirect('offerlist')
        except ValueError:
            messages.error(request, "Invalid price format")
            return redirect('offerlist')
        
        # Save the offer
        new_offer = Offer.objects.create(
            offer_name=offer_name,
            discount_amount=discount_price,
        )
        
        messages.success(request, 'New offer added successfully')
        return redirect('offerlist')
    
    return render(request, 'dashboard/offerlist.html')


def editoffer(request,editoffer_id):
    if request.method == 'POST':
        offer_name = request.POST['offer_name']
        discount_price = request.POST['discount_amount']
# validation
     
        if offer_name == '' or discount_price == '':
            messages.error(request, "Some fields are empty")
            return redirect('offerlist')
        try:
            discount_price = int(discount_price)
            if discount_price < 1:
                  messages.error(request, "Price should be a positive number")
                  return redirect('offerlist')
        except ValueError:
            messages.error(request, "Invalid price format")
            return redirect('offerlist')

        # Save
        
        Offers = Offer.objects.get(id=editoffer_id)
        Offers.offer_name = offer_name
        Offers.discount_amount = discount_price
        Offers.save()
        messages.success(request, "Offer updated successfully")
        return redirect('offerlist')
    
def deleteoffer(request,deleteoffer_id):
    Offers = Offer.objects.get(id=deleteoffer_id)
    Offers.delete()
    messages.success(request, "Offer deleted successfully")
    return redirect('offerlist')
