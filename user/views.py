from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse
from datetime import datetime, timedelta
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from catalog.models import Item, Exchange
from user.models import User, UserComments

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
        "favorites": Item.objects.filter(favorites=request.user, active=True).exclude(seller=request.user),
        "exchanges": Exchange.objects.filter(sent_item__seller=request.user),
    }
    return render(request, "user/checkout.html", context)

def user_details(request, username=None, user_id=None):
    user = get_object_or_404(User, username=username, pk=user_id)
    context = {"user": user}
    return render(request, "user/profile_for_users.html", context)


@login_required
def add_comment(request, user_id=None):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST" and request.user.is_authenticated:
        user_review = request.POST.get("user_review")
        if user_review:
            UserComments.objects.create(from_user=request.user, to_user=user, body=user_review)
            messages.success(request, "Ваше отзыв доставлено")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))




@login_required
def delete_comment(request, comment_id):
    obj = get_object_or_404(UserComments, pk=comment_id)
    if obj.from_user == request.user:
        obj.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@login_required
def user_positive_rating(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_user = request.user

    if current_user in user.user_positive_rating.all():
        user.user_positive_rating.remove(current_user)
    else:
        if current_user in user.user_negative_rating.all():
            user.user_negative_rating.remove(current_user)
        user.user_positive_rating.add(current_user)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@login_required
def user_negative_rating(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_user = request.user

    if current_user in user.user_negative_rating.all():
        user.user_negative_rating.remove(current_user)
    else:
        if current_user in user.user_positive_rating.all():
            user.user_positive_rating.remove(current_user)
        user.user_negative_rating.add(current_user)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
