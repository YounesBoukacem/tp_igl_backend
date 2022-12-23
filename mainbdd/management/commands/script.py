from django.core.management.base import BaseCommand
from mainbdd.models import User, RealEstateAdd, Offer
from mainbdd.factories import UserFactory, RealEstateAddFactory, OfferFactory
import random


class Command(BaseCommand):
    def handle(self, **options):
        # users = []
        # for i in range(10):
        #     users.append(UserFactory())   
        # reas = []
        # for i in range(20):
        #     reas.append(RealEstateAddFactory(owner=random.choice(users)))
        # for user in users:
        #     user.favorits.add(*random.choices(reas,k=random.choice([0,1,2,3,4])))
        for user in User.objects.all():
            for rea in random.choices(RealEstateAdd.objects.exclude(owner_id=user.id), k=random.choice([0,1,2,3])):
                OfferFactory(offerer=user, real_estate=rea)
