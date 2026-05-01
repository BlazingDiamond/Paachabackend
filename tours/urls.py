from django.urls import path


from .views import tour_data_api

urlpatterns = [
    path("api/tour-data/", tour_data_api, name="tour_data_api"),
]
