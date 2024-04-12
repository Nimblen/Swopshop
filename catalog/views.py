from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .utils.services import paginate_objects
from .models import Comment, Item, Photo_of_item, Visit, Exchange
from django.db.models import Count
from .forms import AddMessageForm

# Create your views here.


def index(request):
    return render(request, "index.html")


def shop(request):
    page = request.GET.get("page", 1)
    sort_by = request.GET.get("sort_by", "-date")
    type_by = request.GET.get("type_by", 'all')
    per_page = request.GET.get("per_page", 10)
    items = Item.objects.all()
    my_lots = []
    if request.user.is_authenticated:
        my_lots = items.filter(seller=request.user)[:3]
    if type_by != 'all':
        items = items.filter(type=type_by)
    paginated_items = paginate_objects(items, page, per_page, sort_by)
    context = {"items": paginated_items, 'my_lots': my_lots}
    return render(request, "catalog/shop.html", context)



def item_detail(request, item_slug, item_id):
    item = get_object_or_404(Item, slug=item_slug, pk=item_id)
    photos_of_items = Photo_of_item.objects.filter(item=item)


    if request.method == "POST" and request.user.is_authenticated:
        review = request.POST.get('review')
        if review:
            Comment.objects.create(user=request.user, item=item, body=review)
            messages.success(request, "Ваше отзыв доставлено")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, "catalog/item_detail.html", {"item": item, "photos_of_items": photos_of_items})


def exchange(request, received_item_id):
    si_id = request.GET.get('SI_id', None)
    sent_item = None
    if si_id:
        sent_item = get_object_or_404(Item, pk=si_id)
    received_item = get_object_or_404(Item, pk=received_item_id)
    sent_items_list = Item.objects.filter(seller=request.user)
    context = {"received_item":received_item, "sent_items":sent_items_list, "sent_item":sent_item}
    return render(request, "catalog/exchange.html", context)



def sent_exchange(request, received_item_id, sent_item_id):
    sent_item = get_object_or_404(Item, pk=sent_item_id)
    received_item = get_object_or_404(Item, pk=received_item_id)
    
    ...





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
