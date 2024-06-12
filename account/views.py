from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from .forms import SignUpForm , UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
import json
from cart.cart import Cart

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("Please fill out your information"))

            return redirect('account:update_info')
        
        else:
            messages.success(request, ("please try again there was a problem"))
            return redirect('account:signup')


    else:
        return render(request, 'signup.html', {'form': form })


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)

                cart = Cart(request)

                for key, value in converted_cart.items():
                     cart.db_add(product=key, quantity=value)

                 

        return redirect('products:home')

    else:
        form = AuthenticationForm()
    return render(request,'login.html', {'form':form})


def logout_user(request):
        logout(request)
        return redirect('products:home')
    


def account(request):
    return render(request,'account.html',{} )



def update_user(request):
        if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            user_form = UpdateUserForm(request.POST or None, instance=current_user)

            if user_form.is_valid():
                 user_form.save()

                 login(request, current_user)
                 messages.success(request, "User has been updated")
                 return redirect('products:home')
            return render(request, 'update_user.html', {'user_form': user_form})
             
        else:
            messages.success(request, "You must be logged in")
            return redirect('products:home') 


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method =='POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "You've changed your password,")
                login(request, current_user)
                return redirect('account:account')

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('account:update_password')


        
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in")
        return redirect('products:home')

def update_info(request):
    if request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=request.user.id)
            form = UserInfoForm(request.POST or None, instance=current_user)

            if form.is_valid():
                 form.save()

                 messages.success(request, "Info has been updated")
                 return redirect('account:account')
            return render(request, 'update_info.html', {'form': form})
             
    else:
        messages.success(request, "You must be logged in")
        return redirect('products:home') 