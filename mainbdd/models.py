from django.db import models
from django.contrib import admin

class User (models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone_num = models.CharField(max_length=30)
    favorits = models.ManyToManyField('RealEstateAdd')


    def __str__(self):
        return self.first_name+' '+self.last_name


class RealEstateAdd(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    surface = models.FloatField(null=True)
    price = models.FloatField(null=True)
    pub_date = models.DateField(auto_now_add=True)
    localisation = models.CharField(max_length=300)
    wilaya = models.CharField(max_length=50)
    commune = models.CharField(max_length=50)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ownedReas')
    #Add for later : ImageFiled + Choices for category and type

    def __str__(self):
        return self.title


class Offer(models.Model):
    description = models.TextField()
    proposal = models.FloatField()
    offerer = models.ForeignKey(User,on_delete=models.CASCADE, related_name='offers')
    real_estate = models.ForeignKey(RealEstateAdd,on_delete=models.CASCADE, related_name='offers')
    
    def __str__(self):
        return self.description











# Create your models here.
