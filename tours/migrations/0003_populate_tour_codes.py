from django.db import migrations
import uuid


def generate_code():
    return f"TR-{uuid.uuid4().hex[:4].upper()}"


def populate_tour_codes(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    existing_codes = set(Tour.objects.exclude(tour_instance_code__isnull=True).values_list("tour_instance_code", flat=True))
    for tour in Tour.objects.filter(tour_instance_code__isnull=True):
        code = generate_code()
        while code in existing_codes:
            code = generate_code()
        tour.tour_instance_code = code
        tour.save(update_fields=["tour_instance_code"])
        existing_codes.add(code)


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0002_tour_tour_instance_code"),
    ]

    operations = [
        migrations.RunPython(populate_tour_codes, migrations.RunPython.noop),
    ]
