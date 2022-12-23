from django.contrib import admin
from .models import User, RealEstateAdd, Offer


class OfferInLine(admin.TabularInline):
    model = Offer
    extra = 0

class ReasInLine(admin.TabularInline):
    model = RealEstateAdd
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [ReasInLine]

class RealEstateAddAdmin(admin.ModelAdmin):
    inlines = [OfferInLine]

admin.site.register(User, UserAdmin)
admin.site.register(RealEstateAdd,RealEstateAddAdmin)
admin.site.register(Offer)
# Register your models here.
