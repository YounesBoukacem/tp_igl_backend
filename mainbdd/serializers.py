from rest_framework import serializers
from .models import User, RealEstateAdd, Offer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #We'll start with the none relational fields... i don't think we need
        #_the relational ones ...
        fields = ['id','first_name','last_name','email','phone_num']


class ReaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateAdd
        fields = ['id','title','description','category','type','surface',
        'price','pub_date','localisation','wilaya','commune','owner']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['description','proposal','offerer','real_estate']