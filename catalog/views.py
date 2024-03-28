from django.shortcuts import render

# Create your views here.






def index(request):
    return render(request, 'index.html')




def shop(request):
    return render(request, 'catalog/shop.html')