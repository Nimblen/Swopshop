from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from catalog.models import Item, Exchange
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'login_form': form}
    return render(request, 'user/signin.html', context)





def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'reg_form':form}

    return render(request, 'user/signin.html', context)



# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm( instance=request.user, data = request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = { 'form':form,
#                 'my_items':Item.objects.filter(user=request.user),
#                 'exchange': Exchange.objects.filter(user=request.user)
#                 }
#     return render(request, 'users/profile.html', context)




def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))