from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from user.models import User
from .utils.services import paginate_objects, del_item
from .models import Comment, Item, Photo_of_item, Exchange
from .forms import AddMessageForm, AddItemForm, PhotoFormSet
# Create your views here.


def index(request):
    return render(request, "index.html")


def shop(request):
    category = request.GET.get("category", None)
    page = request.GET.get("page", 1)
    sort_by = request.GET.get("sort_by", "-date")
    type_by = request.GET.get("type_by", "all")
    per_page = request.GET.get("per_page", 10)
    items = Item.objects.filter(active=True)
    if category:
        items = items.filter(category=category)
    my_lots = []
    if request.user.is_authenticated:
        my_lots = items.filter(seller=request.user)[:3]
        items = items.exclude(seller=request.user)
    if type_by != "all":
        items = items.filter(type=type_by)
    paginated_items = paginate_objects(items, page, per_page, sort_by)
    context = {"items": paginated_items, "my_lots": my_lots}
    return render(request, "catalog/shop.html", context)


def like_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user in item.likes.all():
        item.likes.remove(request.user)
    else:
        item.likes.add(request.user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def favorite_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user in item.favorites.all():
        item.favorites.remove(request.user)
    else:
        item.favorites.add(request.user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def item_detail(request, item_slug, item_id):
    item = get_object_or_404(Item, slug=item_slug, pk=item_id)
    photos_of_items = Photo_of_item.objects.filter(item=item)
    if request.method == "POST" and request.user.is_authenticated:
        review = request.POST.get("review")
        if review:
            Comment.objects.create(user=request.user, item=item, body=review)
            messages.success(request, "Ваше отзыв доставлено")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(
        request,
        "catalog/item_detail.html",
        {"item": item, "photos_of_items": photos_of_items},
    )


@login_required
def add_item(request):
    if request.method == "POST":
        form = AddItemForm(data=request.POST)
        formset = PhotoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            for f in formset:
                if f.cleaned_data:
                    photo = f.save(commit=False)
                    photo.item = item
                    photo.save()
            return HttpResponseRedirect(reverse("catalog:shop"))
    form = AddItemForm()
    formset = PhotoFormSet()
    context = {"form": form, "formset": formset}
    return render(request, "catalog/add_item.html", context)


@login_required
def exchange(request, received_item_id):
    si_id = request.GET.get("SI_id", None)
    sent_item = None
    if si_id:
        sent_item = get_object_or_404(Item, pk=si_id)
        if sent_item.seller != request.user:
            sent_item = None
    received_item = get_object_or_404(Item, pk=received_item_id)
    sent_items_list = Item.objects.filter(seller=request.user, active=True)
    context = {
        "received_item": received_item,
        "sent_items": sent_items_list,
        "sent_item": sent_item,
    }
    return render(request, "catalog/exchange.html", context)


@login_required
def send_exchange(request, received_item_id, sent_item_id):
    sent_item = get_object_or_404(Item, pk=sent_item_id)
    received_item = get_object_or_404(Item, pk=received_item_id)
    if request.method == "POST":
        message = request.POST.get("message", "")
        try:
            Exchange.objects.create(
                sent_item=sent_item,
                received_item=received_item,
                status="waiting",
                message=message,
            )
            messages.success(request, "Отправлено")
            return HttpResponseRedirect(reverse("users:profile"))
        except IntegrityError:
            messages.error(request, "Ошибка: обмен уже отправлен")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def change_exchange(request, exchange_id, action):
    exchange = get_object_or_404(Exchange, pk=exchange_id)
    
    if action == "accept":
        accept_exchange(request, exchange)
    if action == "del":
        if exchange.status == "processing":
            decrease_active_deals(exchange.sent_item.seller)
            decrease_active_deals(exchange.received_item.seller)
        delete_exchange(exchange)
        

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def accept_exchange(request, exchange):
    if exchange.status == "waiting":
        exchange.status = "processing"
        exchange.save()
        increase_active_deals(exchange.sent_item.seller)
        increase_active_deals(exchange.received_item.seller)
    elif exchange.status == "processing":
        exchange.status = "complete"
        exchange.save()
        del_item(exchange.sent_item)
        del_item(exchange.received_item)
        decrease_active_deals(exchange.sent_item.seller)
        decrease_active_deals(exchange.received_item.seller)

def delete_exchange(exchange):
    exchange.delete()

def increase_active_deals(user):
    user.active_deals += 1
    user.amount_of_deals += 1
    user.save()

def decrease_active_deals(user):
    user.active_deals -= 1
    user.save()

@login_required
def delete_obj(request, obj_id):
    obj = get_object_or_404(Item, pk=obj_id)
    if obj.seller == request.user:
        del_item(obj)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_comment(request, comment_id):
    obj = get_object_or_404(Comment, pk=comment_id)
    if obj.user == request.user:
        obj.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def contact(request):
    if request.method == "POST":
        comment_form = AddMessageForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.save()
            messages.success(request, "Ваше сообщение доставлено")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    comment_form = AddMessageForm()
    context = {"form": comment_form}
    return render(request, "catalog/contact.html", context)


def search_view(request):
    page = request.GET.get("page", 1)
    sort_by = request.GET.get("sort_by", "-date")
    type_by = request.GET.get("type_by", "all")
    per_page = request.GET.get("per_page", 10)
    word = request.GET.get("q")
    items = None
    users = None
    if word:
        items = Item.objects.filter(name__iregex=word)
        if type_by != "all":
            items = items.filter(type=type_by)
        paginated_items = paginate_objects(items, page, per_page, sort_by)

        users = User.objects.filter(
            Q(first_name__iregex=word) | Q(last_name__iregex=word)
        )

    context = {
        "title": "Результаты поиска",
        "found_items": paginated_items,
        "found_users": users,
    }

    return render(request, "catalog/search_result.html", context)
