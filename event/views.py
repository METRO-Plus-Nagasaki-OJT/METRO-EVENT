from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
from django.db.models import Count, Case, When, IntegerField, Value, Sum
from django.utils import timezone
from datetime import datetime


# Create your views here.
def index(request):

    if request.method == "POST":
        name = request.POST.get("name")
        start = datetime.strptime(request.POST.get("starttime"), "%Y-%m-%dT%H:%M")

        end = datetime.strptime(request.POST.get("endtime"), "%Y-%m-%dT%H:%M")
        print(start, "-", end)
        venue = request.POST.get("venue")
        organizer_id = request.POST.get("organizer")
        memo = request.POST.get("memo")
        organizer = User.objects.get(id=organizer_id)
        event = Event(
            name=name,
            start_time=start,
            end_time=end,
            venue=venue,
            memo=memo,
            admin=organizer,
        )
        event.save()
        return JsonResponse({"success": "True"})
    current_time = timezone.now()
    events = (
        Event.objects.annotate(
            participant_count=Count("participant"),
            attendance_count=Count("participant__attendances"),
        )
        .values(
            "id",
            "name",
            "start_time",
            "end_time",
            "participant_count",
            "attendance_count",
        )
        .order_by("id")
    )
    for event in events:
        if event["start_time"] <= current_time <= event["end_time"]:
            event["status"] = "Open"
        elif current_time > event["end_time"]:
            event["status"] = "Closed"
        else:
            event["status"] = "Upcoming"

    context = {"event": events, "user": User.objects.all()}

    return render(request, "event/index.html", context)


def edit(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        # Get form data
        name = request.POST.get("editname")
        start_time = datetime.strptime(request.POST.get("start_time"), "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(request.POST.get("end_time"), "%Y-%m-%dT%H:%M")
        venue = request.POST.get("editvenue")
        organizer_id = request.POST.get("editorganizer")
        memo = request.POST.get("editmemo")

        # Validate and assign new values to the event instance
        event.name = name if name else event.name
        event.start_time = start_time if start_time else event.start_time
        event.end_time = end_time if end_time else event.end_time
        event.venue = venue if venue else event.venue
        event.memo = memo if memo else event.memo

        # Fetch the user object based on the organizer_id
        if organizer_id:
            try:
                event.admin = User.objects.get(id=organizer_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "Organizer does not exist."}, status=400)

        event.save()
        return JsonResponse({"message": "Event updated successfully."})

    else:
        users = User.objects.all()

        print(event.start_time.strftime("%Y/%m/%d %H:%M:%S"))
        print(event.start_time)
        context = {
            "name": event.name,
            "created_at": event.toLocaleString(event.start_time),
            "updated_at": event.toLocaleString(event.end_time),
            "venue": event.venue,
            "memo": event.memo,
            "user_id": event.admin.id,
        }
        return JsonResponse(context)


def delete(request, id):
    if request.method == "POST":
        product = get_object_or_404(Event, id=id)
        product.delete()
        return redirect(
            "event"
        )  # Redirect to the product list page or another page after deletion
    context = {"event": Event.objects.all()}
    return JsonResponse(context)


def update_v2(request, id):
    if request.method == "POST":
        obj = {}
        name = request.POST.get("name")
        user = request.POST.get("user")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        venue = request.POST.get("venue")
        memo = request.POST.get("memo")

        if name:
            obj["name"] = name

        if start_time:
            obj["start_time"] = start_time

        if end_time:
            obj["end_time"] = end_time

        if venue:
            obj["venue"] = venue

        if memo:
            obj["memo"] = venue

        try:
            user = User.objects.get(id=user)
            obj["admin"] = user
        except User.DoesNotExist:
            pass

        Event.objects.filter(id=id).update(**obj)

        try:
            event = Event.objects.annotate(
                participant_count=Count("participant"),
                attendance_entry_1_count=Sum(
                    Case(
                        When(
                            participant__attendances__entry_1__isnull=False,
                            then=Value(1),
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
            ).get(id=id)
            data = {
                "id": event.id,
                "name": event.name,
                "date": event.date,
                "attendance": f"{event.participant_count}/{event.attendance_entry_1_count}",
                "status": event.status,
                "start_time": event.locale_format_start_time,
                "end_time": event.locale_format_end_time,
                "venue": event.venue,
            }
            return JsonResponse({"event": data})
        except Event.DoesNotExist:
            return JsonResponse({"event": None})


def index_v2(request):
    if request.method == "POST":
        name = request.POST.get("name")
        user = request.POST.get("user")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        venue = request.POST.get("venue")
        memo = request.POST.get("memo")
        organizer = User.objects.get(id=user)

        event = Event(
            name=name,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            memo=memo,
            admin=organizer,
        )
        event.save()

        event = Event.objects.annotate(
            participant_count=Count("participant"),
            attendance_entry_1_count=Sum(
                Case(
                    When(
                        participant__attendances__entry_1__isnull=False,
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        ).get(id=event.id)

        event = {
            "id": event.id,
            "name": event.name,
            "date": event.date,
            "attendance": f"{event.participant_count}/{event.attendance_entry_1_count}",
            "status": event.status,
            "start_time": event.locale_format_start_time,
            "end_time": event.locale_format_end_time,
            "venue": event.venue,
        }

        return JsonResponse({"event": event})

    if request.headers["Accept"] != "application/json":
        # if request.GET.get("page"):
        #     page = request.GET.get("page")
        # if request.GET.get("limit"):
        #     limit = request.GET.get("limit")
        # if request.GET.get("order"):
        #     pass
        # else:
        #     events = events.order_by("-created_at")

        # paginator = Paginator(events, limit)

        # try:
        #     event_page = paginator.page(page)
        # except PageNotAnInteger:
        #     event_page = paginator.page(1)
        # except EmptyPage:
        #     event_page = paginator.page(paginator.num_pages)

        # total = Event.objects.count()
        # start = (event_page.number - 1) * limit + 1
        # to = (event_page.number - 1) * limit + limit
        # context = {
        #     "event_page": event_page,
        #     "paginator": paginator,
        #     "from": start,
        #     "to": total if to > total else to,
        #     "total": total,
        # }

        return render(
            request, "event/index_v2.html", context={"users": User.objects.filter()}
        )
    elif request.headers["Accept"] == "application/json":
        events = Event.objects.annotate(
            participant_count=Count("participant"),
            attendance_entry_1_count=Sum(
                Case(
                    When(
                        participant__attendances__entry_1__isnull=False,
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        ).filter()
        events = events.order_by("-created_at")
        data = []
        for event in events:
            data.append(
                {
                    "id": event.id,
                    "name": event.name,
                    "date": event.date,
                    "attendance": f"{event.participant_count}/{event.attendance_entry_1_count}",
                    "status": event.status,
                    "start_time": event.locale_format_start_time,
                    "end_time": event.locale_format_end_time,
                    "venue": event.venue,
                }
            )

        return JsonResponse({"events": data})
