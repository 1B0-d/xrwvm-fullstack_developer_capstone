from django.db import transaction

from .models import CarMake, CarModel


@transaction.atomic
def initiate():
    """Populate the sample catalogue only when it is empty."""
    if CarMake.objects.exists():
        return
    makes = [
        ('NISSAN', 'Great cars. Japanese technology', ['Pathfinder', 'Qashqai', 'XTRAIL']),
        ('Mercedes', 'Great cars. German technology', ['A-Class', 'C-Class', 'E-Class']),
        ('Audi', 'Great cars. German technology', ['A4', 'A5', 'A6']),
        ('Kia', 'Great cars. Korean technology', ['Sorrento', 'Carnival', 'Cerato']),
        ('Toyota', 'Great cars. Japanese technology', ['Corolla', 'Camry', 'Kluger']),
    ]
    for make_name, description, names in makes:
        make = CarMake.objects.create(name=make_name, description=description)
        for name in names:
            kind = 'Sedan' if name in ('Cerato', 'Corolla', 'Camry') else 'SUV'
            CarModel.objects.create(name=name, car_make=make, type=kind, year=2023)
