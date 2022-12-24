from django.contrib import admin
from .models import User, RealEstateAdd, Offer


class OfferInLine(admin.TabularInline):
    model = Offer
    extra = 0

class ReasInLine(admin.TabularInline):
    model = RealEstateAdd
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display=('__str__','id')
    readonly_fields=('id',)
    inlines = [ReasInLine]

class RealEstateAddAdmin(admin.ModelAdmin):
    list_display=('__str__','id')
    readonly_fields=('id',)
    inlines = [OfferInLine]

class OfferAdmin(admin.ModelAdmin):
    list_display=('__str__','id')
    readonly_fields=('id',)

admin.site.register(User, UserAdmin)
admin.site.register(RealEstateAdd,RealEstateAddAdmin)
admin.site.register(Offer, OfferAdmin)
# Register your models here.
