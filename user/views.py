from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse
from datetime import datetime, timedelta
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from catalog.models import Item, Exchange

# Create your views here.


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("index"))
    else:
        form = UserLoginForm()

    context = {"login_form": form}
    return render(request, "user/signin.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.ip_address = request.META.get("REMOTE_ADDR")
            user.save()
            messages.success(request, "Регистрация прошла успешно!")
            return HttpResponseRedirect(reverse("users:login"))
    else:
        form = UserRegistrationForm()
    context = {"reg_form": form}

    return render(request, "user/signin.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(
            instance=request.user, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = UserProfileForm(instance=request.user)
    items = Item.objects.filter(
        active=False, deactivate_date__lt=datetime.now() - timedelta(days=30)
    )
    for item in items:
        item.delete()
    context = {
        "form": form,
        "my_items": Item.objects.filter(seller=request.user, active=True),
        "exchanges": Exchange.objects.filter(sent_item__seller=request.user),
    }
    return render(request, "user/checkout.html", context)


def exchanges(request):
    exchanges = Exchange.objects.filter(sent_item__seller=request.user)
    context = {"exchanges": exchanges}
    return render(request, "user/exchanges.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))
