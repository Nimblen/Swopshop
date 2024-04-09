from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger






def paginate_objects(objects, page_number, per_page):
    paginator = Paginator(objects, per_page)
    try:
        paginated_objects = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)
    return paginated_objects