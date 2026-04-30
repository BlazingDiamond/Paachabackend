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


class Tour(models.Model):
    tour_instance_code = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
    )
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    max_guests = models.PositiveIntegerField(default=10)
    available_slots = models.PositiveIntegerField(default=10)
    price_zar = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_start"]

    def __str__(self):
        return f"{self.tour_instance_code} - {self.title} ({self.location})"

    def clean(self):
        if self.scheduled_end <= self.scheduled_start:
            raise ValidationError("scheduled_end must be after scheduled_start.")

        overlapping = Tour.objects.filter(
            is_active=True,
            scheduled_start__lt=self.scheduled_end,
            scheduled_end__gt=self.scheduled_start,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This schedule overlaps with an existing active tour.")

    def save(self, *args, **kwargs):
        if not self.tour_instance_code:
            self.tour_instance_code = generate_tour_instance_code()
        if self.available_slots > self.max_guests:
            self.available_slots = self.max_guests
        self.full_clean()
        super().save(*args, **kwargs)


class TourBooking(models.Model):
    class PaymentGateway(models.TextChoices):
        PAYFAST = "payfast", "PayFast"
        PEACH = "peach", "Peach Payments"
        YOCO = "yoco", "Yoco"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    guests = models.PositiveIntegerField(default=1)
    payment_gateway = models.CharField(
        max_length=20,
        choices=PaymentGateway.choices,
        default=PaymentGateway.PAYFAST,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    tour_code = models.CharField(max_length=30, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.tour.title}"

    def save(self, *args, **kwargs):
        if not self.tour_code:
            self.tour_code = generate_tour_code()
        super().save(*args, **kwargs)
