from django.contrib import admin
from .models import *


class BikesInline(admin.TabularInline):
    model = Bike
    fields = ('name', 'brand', 'model',)


class BikeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'brand',
                    'model',
                    'made_year',
                    )
    ordering = ('pk',)
    list_filter = ('model',)


class OwnerAdmin(admin.ModelAdmin):
    inlines = [BikesInline]


admin.site.register(Bike, BikeAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Ownership)
