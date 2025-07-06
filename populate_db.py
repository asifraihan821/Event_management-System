import os
import django

# settings pointing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

from events.models import Event, Category, Participants
from faker import Faker
import random

fake = Faker()

# Create some fake categories
categories = []
for _ in range(5):
    category = Category.objects.create(
        name=fake.word(),
        description=fake.sentence()
    )
    categories.append(category)

# Create fake events
for _ in range(10):
    event = Event.objects.create(
        name=fake.sentence(nb_words=3),
        description=fake.text(),
        date=fake.date_this_year(),
        location=fake.city(),
        category=random.choice(categories)
    )

# Create fake participants and assign events
for _ in range(15):
    participant = Participants.objects.create(
        name=fake.name(),
        email=fake.email()
    )
    participant.event.set(random.sample(list(Event.objects.all()), k=2))
