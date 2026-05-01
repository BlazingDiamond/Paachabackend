from django.http import JsonResponse
from .models import Country, Pin, Tour


def tour_data_api(request):
    # Fetch all data from DB
    db_countries = Country.objects.all()
    db_pins = Pin.objects.all()
    db_tours = Tour.objects.filter(is_active=True).select_related(
        "country", "center_pin"
    )

    # 1. Build Countries Object
    countries_dict = {}
    for c in db_countries:
        countries_dict[c.id_code] = {
            "id": c.id_code,
            "name": c.name,
            "flag": c.flag,
            "tagline": c.tagline,
            "cardImage": c.card_image,
            "heroImage": c.hero_image,
            "center": [c.center_lat, c.center_lon],
            "zoom": c.zoom,
            "topoId": c.topo_id,
            "color": c.color,
            "description": c.description,
        }

    # 2. Build Pins Object
    pins_dict = {}
    for p in db_pins:
        pins_dict[p.slug] = {
            "lat": p.lat,
            "lon": p.lon,
            "label": p.label,
            "country": p.country.id_code,
        }

    # 3. Build Tours Lists
    city_tours = []
    country_tours = []

    for t in db_tours:
        tour_obj = {
            "id": f"tour-{t.id}",
            "country": t.country.id_code,
            "type": t.type,
            "name": t.name,
            "tagline": t.tagline,
            "heroImage": t.hero_image,
            "duration": t.duration,
            "bestTime": t.best_time,
            "groupSize": t.group_size,
            "startingFrom": f"{t.currency} {t.starting_from}",
            "currency": t.currency,
            "rating": t.rating,
            "reviewCount": t.review_count,
            "centerPin": t.center_pin.slug if t.center_pin else "",
            "highlights": t.highlights,
            "included": t.included,
            "notIncluded": t.not_included,
            "photos": t.photos,
            "itinerary": t.itinerary,
        }

        if t.type in ["city", "landmark"]:
            city_tours.append(tour_obj)
        else:
            # For multi-city, add the totalDays helper (extracts digit from '7 days')
            days_val = "".join(filter(str.isdigit, t.duration))
            tour_obj["totalDays"] = int(days_val) if days_val else 0
            country_tours.append(tour_obj)

    # Final Output
    return JsonResponse(
        {
            "countries": countries_dict,
            "pins": pins_dict,
            "cityTours": city_tours,
            "countryTours": country_tours,
        },
        safe=False,
    )
