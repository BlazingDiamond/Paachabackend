from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import secrets
import uuid


def generate_tour_code():
    token = secrets.token_hex(2).upper()
    return f"TOURS-{timezone.now().year}-{token}"


def generate_tour_instance_code():
    return f"TR-{uuid.uuid4().hex[:4].upper()}"


# --- SIMPLIFIED TOUR MODEL ---

# --- EXPANDED TOUR MODEL ---
from django.contrib.postgres.fields import ArrayField


class Country(models.Model):
    id_code = models.CharField(
        max_length=2, primary_key=True, help_text="ISO Code (e.g., ZA, ZW)"
    )
    name = models.CharField(max_length=100)
    flag = models.CharField(max_length=10, help_text="Emoji flag (e.g., 🇿🇦)")
    tagline = models.CharField(max_length=200)
    card_image = models.CharField(max_length=500)
    hero_image = models.CharField(max_length=500)
    center_lat = models.FloatField(default=0.0)
    center_lon = models.FloatField(default=0.0)
    zoom = models.IntegerField(default=5)
    topo_id = models.CharField(max_length=10, help_text="ISO alpha-3 (e.g., ZAF)")
    color = models.CharField(
        max_length=7, default="#5c7a3e", help_text="Hex color code"
    )
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} ({self.id_code})"


class Pin(models.Model):
    slug = models.SlugField(
        primary_key=True, help_text="Unique ID for map (e.g., cape-town)"
    )
    label = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="pins")

    def __str__(self):
        return self.label


class Tour(models.Model):
    TOUR_TYPE_CHOICES = [
        ("city", "City"),
        ("landmark", "Landmark"),
        ("multi-city", "Multi-City"),
        ("multi-country", "Multi-Country"),
    ]

    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TOUR_TYPE_CHOICES, default="city")
    tagline = models.CharField(max_length=200, blank=True)
    hero_image = models.URLField(blank=True)
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., '3-7 days'")
    best_time = models.CharField(
        max_length=50, blank=True, help_text="e.g., 'Oct - Apr'"
    )
    group_size = models.CharField(max_length=50, blank=True)
    starting_from = models.CharField(
        max_length=50, blank=True, help_text="Just the number, e.g., '245'"
    )
    currency = models.CharField(max_length=10, default="USD")
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    center_pin = models.ForeignKey(
        Pin, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True)

    # JSON Fields for complex data
    highlights = models.JSONField(
        default=list,
        blank=True,
        help_text='List of {"icon": "🏔️", "text": "..."} objects',
    )
    included = models.JSONField(default=list, blank=True)
    not_included = models.JSONField(default=list, blank=True)
    photos = models.JSONField(default=list, blank=True)
    itinerary = models.JSONField(
        default=list,
        blank=True,
        help_text='List of {"day": 1, "title": "...", "desc": "...", "pin": "slug", "img": "url"}',
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country.id_code})"
