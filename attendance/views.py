from django.shortcuts import render, get_object_or_404, redirect
from event.models import Event
from .models import Attendance
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.db.models import Case, When, IntegerField
from django.http import JsonResponse

# Create your views here.


def index(request):
    if request.method == "GET":
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
        if request.GET.get("name"):
            filters &= Q(participant__name__icontains=request.GET.get("name"))
        if request.GET.get("date"):
            date_range = []
            for k, value in enumerate(request.GET.get("date").split(",")):
                time = "00:00:00"
                if k == 1:
                    time = "23:59:59"
                date_range.append(
                    datetime.strptime(f"{value} {time}", "%Y/%m/%d %H:%M:%S")
                )
            if len(date_range) == 1:
                filters &= Q(created_at__gte=date_range[0])
            else:
                filters &= Q(created_at__range=date_range)
        else:
            first_day_of_the_current_month = timezone.now().replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            filters &= Q(created_at__gte=first_day_of_the_current_month)

        attendances = (
            Attendance.objects.annotate(
                status=Case(
                    When(entry_1__isnull=False, leave_1__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            )
            .filter(filters)
            .prefetch_related("participant")
        )

        if request.GET.get("sort"):
            attendances = attendances.order_by(request.GET.get("sort"))

        paginator = Paginator(attendances, limit)

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


def update(request, id):
    if request.method == "POST":
        obj = {}
        if request.POST.get("entry_1"):
            obj["entry_1"] = request.POST.get("entry_1")

        if request.POST.get("leave_1"):
            obj["leave_1"] = request.POST.get("leave_1")

        if request.POST.get("entry_2"):
            obj["entry_2"] = request.POST.get("entry_2")

        if request.POST.get("leave_1"):
            obj["leave_2"] = request.POST.get("leave_2")

        if len(obj.keys()):
            Attendance.objects.filter(id=id).update(**obj)
        if request.headers["Accept"] == "application/json" :
           return JsonResponse({
                "attendance": Attendance.objects.filter(id=id).values()[0] or None
           })
        messages.success(request, "Attendance updated.")
        return redirect(request.META.get("HTTP_REFERER", "/"))


def index_v2(request):
    if request.method == "GET":
        events = Event.objects.all()
        if request.headers["Accept"] != "application/json":
            return render(request, "attendance/index_v2.html", {"events": events})

        filters = Q()
        limit = 10

        if request.GET.get("page"):
            page = request.GET.get("page")
        if request.GET.get("limit"):
            limit = request.GET.get("limit")
        if request.GET.get("event"):
            filters &= Q(participant__event=request.GET.get("event"))
        if request.GET.get("name"):
            filters &= Q(participant__name__icontains=request.GET.get("name"))
        if request.GET.get("date"):
            date_range = []
            for k, value in enumerate(request.GET.get("date").split(",")):
                time = "00:00:00"
                if k == 1:
                    time = "23:59:59"
                date_range.append(
                    datetime.strptime(f"{value} {time}", "%Y/%m/%d %H:%M:%S")
                )
            if len(date_range) == 1:
                filters &= Q(created_at__gte=date_range[0])
            else:
                filters &= Q(created_at__range=date_range)
        else:
            first_day_of_the_current_month = timezone.now().replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            print(first_day_of_the_current_month)
            filters &= Q(created_at__gte=first_day_of_the_current_month)

        attendances = (
            Attendance.objects.annotate(
                status=Case(
                    When(entry_1__isnull=False, leave_1__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            )
            .filter(filters)
            .prefetch_related("participant")
        )

        data = []
        for attendance in attendances:
            data.append({
                'id': attendance.id,
                'status': attendance.status,
                'participant': {
                    'id': attendance.participant.id,
                    'name': attendance.participant.name,  
                },
                'entry_1': attendance.entry_1,
                'leave_1': attendance.leave_1,
                'entry_2': attendance.entry_2,
                'leave_2': attendance.leave_2,
                'date': attendance.date
            })

        return JsonResponse({"attendances": data, "limit": int(limit)})
