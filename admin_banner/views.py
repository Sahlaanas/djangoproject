from django.shortcuts import render, redirect
from user_home.models import Banner
from django.contrib import messages
from user_category.models import Category

# Create your views here.
def bannerlist(request):
      query = request.GET.get('query')
      if query:
            banner = Banner.objects.filter(banner_name__icontains=query)
      else:
            banner = Banner.objects.all()
      category = Category.objects.all()
      context = {
            'banner' : banner,
            'category' : category
      }
      return render(request, 'dashboard/bannerlist.html', context)

def addbanner(request):
    if request.method == 'POST':
        name = request.POST['banner_name']
        description = request.POST['banner_description']
        category_id= request.POST['category']
        image = request.FILES.get('image', None)
        
        # Validation
        if Banner.objects.filter(banner_name=name).exists():
            messages.error(request, 'Banner name already exists')
            return redirect('bannerlist')
        if name == '' or category_id == '' or description =='':
            messages.error(request, "Some fields are empty")
            return redirect('bannerlist')
        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('bannerlist')
      
        categorys = Category.objects.get(id=category_id)
        
        # Save the brand
        new_banner = Banner.objects.create(
            banner_name=name,
            banner_description=description,
            banner_image=image,
            Category=categorys,
        )
        messages.success(request, 'Banner added successfully')
        return redirect('bannerlist')
        
    return render(request, 'dashboard/bannerlist.html',new_banner)



def editbanner(request,editbanner_id):
    if request.method == 'POST':
        name = request.POST['banner_name']
        description = request.POST['banner_description']
        category_id = request.POST['category']
        
# validation
     

        if name == ''  or description == '' or category_id=='':
            messages.error(request, "Some field are empty")
            return redirect('bannerlist')
        try:
            Banners = Banner.objects.get(id=editbanner_id)
            eimage = request.FILES.get('image')
            if eimage:
                Banners.banner_image = eimage
                Banners.save()
        except Banner.DoesNotExist:
            messages.error(request, "Image not found")
            return redirect('bannerlist')
        
        # Save
        
        categorys = Category.objects.get(id=category_id)
        Banners = Banner.objects.get(id=editbanner_id)
        Banners.banner_name = name
        Banners.banner_description = description
        Banners.Category= categorys
        
        Banners.save()
        return redirect('bannerlist')
    
def deletebanner(request,deletebanner_id):
    Banners = Banner.objects.get(id=deletebanner_id)
    Banners.delete()
    return redirect('bannerlist')
