from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count






def paginate_objects(objects, page_number, per_page, sort_by='id'):
    if sort_by == 'likes':
        objects = objects.annotate(likes_count=Count('likes')).order_by('-likes_count')
    elif sort_by == '-likes':
        objects = objects.annotate(likes_count=Count('likes')).order_by('likes_count')
    else:
        objects = objects.order_by(sort_by)
    paginator = Paginator(objects, per_page)
    try:
        paginated_objects = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)
    return paginated_objects




def del_item(obj):
    obj.active = False
    obj.deactivate_date = datetime.now()
    return obj.save()
