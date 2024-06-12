from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def home(request):
    product = Product.objects.all()
    context = {'products': product}
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def clothes(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'items.html', context)


def category(request,nme):
    try:
        category = Category.objects.get(name=nme) 
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'categorys':category})
    except:
        return redirect('products:home')



def search_results(request):
    if request.method == "POST":
        searched = request.POST['searched']

        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.success(request, "That Product Does Not Exist, Please Try Again")
            return render(request, 'search_results.html', {})
        else:
            return render(request, 'search_results.html', {'searched': searched })
    else:
        return render(request, 'search_results.html', {})
