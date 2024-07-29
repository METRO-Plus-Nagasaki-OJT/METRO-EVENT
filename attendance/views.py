from django.shortcuts import render
from event.models import Event
from .models import Attendance
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

# Create your views here.


def index(request):
    events = Event.objects.all()

    filters = Q()

    page = 1

    limit = 10

    if request.GET.get("page"):
        page = request.GET.get("page")

    if request.GET.get("limit"):
        limit = request.GET.get("limit")

    if request.GET.get("event"):
        filters &= Q(participant__event=request.GET.get("event"))
    if request.GET.get("date"):
        date_range = []
        for d in request.GET.get("date").split(","):
            date_range.append(datetime.strptime(f"{d} 24:59:59", "%Y/%m/%d %H:%M:%S"))

        if len(date_range) == 1:
            filters &= Q(created_at__gte=date_range[0])
        else:
            filters &= Q(created_at__range=date_range)

    attendaces = Attendance.objects.filter(filters)

    paginator = Paginator(attendaces, limit)

    try:
        attendances_page = paginator.page(page)
    except PageNotAnInteger:
        attendances_page = paginator.page(1)
    except EmptyPage:
        attendances_page = paginator.page(paginator.num_pages)

    context = {
        "events": events,
        "attendances": attendances_page,
        "paginator": paginator,
    }

    return render(request, "attendance/index.html", context)
