from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def products(request):
    return render(request, 'products.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'aboutus.html')

def metal(request):
    return render(request, 'metal.html')

def agro_commodities(request):
    return render(request, 'agro_commodities.html')

def industrialproduct(request):
    return render(request, 'industrialproduct.html')

def frozen_foods(request):
    return render(request, 'frozen_foods.html')


