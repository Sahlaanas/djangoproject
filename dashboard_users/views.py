from django.shortcuts import render

# Create your views here.
def adminprofile(request):
    return render(request, 'dashboard/adminprofile.html')