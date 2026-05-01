from django.contrib import admin
<<<<<<< HEAD
from .models import Tour, TourBooking
=======
from .models import Country, Pin, Tour


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id_code", "name", "flag")


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "country")
    list_filter = ("country",)
    search_fields = ("label", "slug")
>>>>>>> f0bfb8c (first commit on other laptop)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
<<<<<<< HEAD
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
=======
    list_display = ("name", "country", "type", "is_active")
    list_filter = ("country", "type", "is_active")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "country", "type", "tagline", "is_active")},
        ),
        (
            "Pricing & Stats",
            {
                "fields": (
                    "starting_from",
                    "currency",
                    "duration",
                    "group_size",
                    "best_time",
                    "rating",
                    "review_count",
                )
            },
        ),
        ("Media", {"fields": ("hero_image", "photos", "center_pin")}),
        (
            "Rich Content (JSON)",
            {
                "description": "Ensure you use valid JSON format for these fields.",
                "fields": (
                    "highlights",
                    "included",
                    "not_included",
                    "itinerary",
                    "description",
                ),
            },
        ),
    )
>>>>>>> f0bfb8c (first commit on other laptop)
