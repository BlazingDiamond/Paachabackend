from datetime import timedelta
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_GET, require_http_methods

from accounts.auth import parse_json_body, token_auth_required
from .models import Tour, TourBooking


def serialize_tour(tour):
    return {
        "id": tour.id,
        "tour_instance_code": tour.tour_instance_code,
        "title": tour.title,
        "location": tour.location,
        "description": tour.description,
        "scheduled_start": tour.scheduled_start.isoformat(),
        "scheduled_end": tour.scheduled_end.isoformat(),
        "available_slots": tour.available_slots,
        "max_guests": tour.max_guests,
        "price_zar": str(tour.price_zar),
        "is_active": tour.is_active,
    }


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def date_span(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


@require_GET
def schedule_list_api(request):
    tours = Tour.objects.filter(is_active=True).order_by("scheduled_start")
    payload = [serialize_tour(tour) for tour in tours]
    return JsonResponse({"tours": payload})


@require_GET
def schedule_calendar_api(request):
    tours = Tour.objects.filter(is_active=True).order_by("scheduled_start")
    events = [
        {
            "tour_id": tour.id,
            "tour_instance_code": tour.tour_instance_code,
            "title": tour.title,
            "start": tour.scheduled_start.isoformat(),
            "end": tour.scheduled_end.isoformat(),
        }
        for tour in tours
    ]
    busy_dates = sorted(
        {
            day.isoformat()
            for tour in tours
            for day in date_span(tour.scheduled_start.date(), tour.scheduled_end.date())
        }
    )
    return JsonResponse({"events": events, "busy_dates": busy_dates})


@require_GET
def availability_api(request):
    start_raw = request.GET.get("start")
    end_raw = request.GET.get("end")
    if not start_raw or not end_raw:
        return JsonResponse({"detail": "Provide start and end query params in ISO datetime format."}, status=400)

    start_dt = parse_datetime(start_raw)
    end_dt = parse_datetime(end_raw)
    if not start_dt or not end_dt:
        return JsonResponse({"detail": "Invalid datetime format. Use ISO datetime values."}, status=400)
    if end_dt <= start_dt:
        return JsonResponse({"detail": "end must be after start."}, status=400)

    overlaps = Tour.objects.filter(
        is_active=True,
        scheduled_start__lt=end_dt,
        scheduled_end__gt=start_dt,
    ).order_by("scheduled_start")
    return JsonResponse(
        {
            "requested_start": start_dt.isoformat(),
            "requested_end": end_dt.isoformat(),
            "is_available": not overlaps.exists(),
            "conflicts": [serialize_tour(tour) for tour in overlaps],
        }
    )


@require_http_methods(["POST"])
@token_auth_required
def schedule_create_api(request):
    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    required_fields = ["title", "location", "scheduled_start", "scheduled_end", "price_zar"]
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return JsonResponse({"detail": f"Missing required fields: {', '.join(missing)}"}, status=400)

    scheduled_start = parse_datetime(payload["scheduled_start"])
    scheduled_end = parse_datetime(payload["scheduled_end"])
    if not scheduled_start or not scheduled_end:
        return JsonResponse({"detail": "scheduled_start and scheduled_end must be ISO datetime strings."}, status=400)

    max_guests = int(payload.get("max_guests", 10))
    available_slots = int(payload.get("available_slots", max_guests))
    if available_slots > max_guests:
        available_slots = max_guests

    try:
        tour = Tour.objects.create(
            title=payload["title"].strip(),
            location=payload["location"].strip(),
            description=(payload.get("description") or "").strip(),
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            max_guests=max_guests,
            available_slots=available_slots,
            price_zar=payload["price_zar"],
            is_active=parse_bool(payload.get("is_active", True)),
        )
    except ValidationError as exc:
        return JsonResponse({"detail": exc.messages}, status=400)
    return JsonResponse({"tour": serialize_tour(tour)}, status=201)


@require_http_methods(["PUT", "PATCH", "DELETE"])
@token_auth_required
def schedule_detail_api(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)

    if request.method == "DELETE":
        tour.delete()
        return JsonResponse({}, status=204)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    fields = {
        "title": str,
        "location": str,
        "description": str,
        "price_zar": str,
        "max_guests": int,
        "available_slots": int,
    }
    for key, caster in fields.items():
        if key in payload and payload[key] is not None:
            setattr(tour, key, caster(payload[key]))
    if "is_active" in payload:
        tour.is_active = parse_bool(payload["is_active"])

    if "scheduled_start" in payload:
        parsed = parse_datetime(payload["scheduled_start"])
        if not parsed:
            return JsonResponse({"detail": "Invalid scheduled_start datetime."}, status=400)
        tour.scheduled_start = parsed
    if "scheduled_end" in payload:
        parsed = parse_datetime(payload["scheduled_end"])
        if not parsed:
            return JsonResponse({"detail": "Invalid scheduled_end datetime."}, status=400)
        tour.scheduled_end = parsed

    if tour.available_slots > tour.max_guests:
        tour.available_slots = tour.max_guests
    try:
        tour.save()
    except ValidationError as exc:
        return JsonResponse({"detail": exc.messages}, status=400)
    return JsonResponse({"tour": serialize_tour(tour)})


@require_http_methods(["POST"])
def booking_create_api(request):
    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    tour = get_object_or_404(Tour, pk=payload.get("tour_id"), is_active=True)
    guests = max(int(payload.get("guests", 1)), 1)
    if guests > tour.available_slots:
        return JsonResponse({"detail": "Not enough available slots for this tour."}, status=400)

    booking = TourBooking.objects.create(
        tour=tour,
        full_name=(payload.get("full_name") or "").strip(),
        email=(payload.get("email") or "").strip(),
        guests=guests,
        payment_gateway=payload.get("payment_gateway", TourBooking.PaymentGateway.PAYFAST),
    )
    tour.available_slots -= guests
    tour.save(update_fields=["available_slots"])
    return JsonResponse(
        {
            "booking": model_to_dict(
                booking,
                fields=["id", "full_name", "email", "guests", "payment_gateway", "payment_status", "tour_code"],
            )
        },
        status=201,
    )
