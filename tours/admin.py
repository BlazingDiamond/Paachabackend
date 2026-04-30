from django.contrib import admin
from .models import Tour, TourBooking


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "tour_instance_code",
        "title",
        "location",
        "scheduled_start",
        "scheduled_end",
        "available_slots",
        "price_zar",
        "is_active",
    )
    list_filter = ("is_active", "location", "scheduled_start")
    search_fields = ("tour_instance_code", "title", "location")
    readonly_fields = ("tour_instance_code",)
    ordering = ("scheduled_start",)


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = (
        "tour",
        "full_name",
        "email",
        "guests",
        "payment_gateway",
        "payment_status",
        "tour_code",
        "created_at",
    )
    list_filter = ("payment_gateway", "payment_status", "created_at")
    search_fields = ("full_name", "email", "tour_code", "tour__title")
    readonly_fields = ("tour_code", "created_at")
