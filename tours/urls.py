from django.urls import path

from .views import (
    availability_api,
    booking_create_api,
    schedule_calendar_api,
    schedule_create_api,
    schedule_detail_api,
    schedule_list_api,
)

urlpatterns = [
    path("api/tours/schedule/", schedule_list_api, name="tour-schedule-api"),
    path("api/tours/calendar/", schedule_calendar_api, name="tour-schedule-calendar-api"),
    path("api/tours/availability/", availability_api, name="tour-availability-api"),
    path("api/tours/schedule/create/", schedule_create_api, name="tour-schedule-create-api"),
    path("api/tours/schedule/<int:tour_id>/", schedule_detail_api, name="tour-schedule-detail-api"),
    path("api/tours/bookings/create/", booking_create_api, name="tour-booking-create-api"),
]
