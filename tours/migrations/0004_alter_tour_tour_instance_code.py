from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0003_populate_tour_codes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tour",
            name="tour_instance_code",
            field=models.CharField(editable=False, max_length=12, unique=True),
        ),
    ]
