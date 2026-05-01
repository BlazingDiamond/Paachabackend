from django.contrib import admin
from .models import Country, Pin, Tour


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id_code", "name", "flag")


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "country")
    list_filter = ("country",)
    search_fields = ("label", "slug")


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
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
