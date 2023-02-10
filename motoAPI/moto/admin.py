from django.contrib import admin
from .models import *


class BikeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'brand',
                    'model',
                    'made_year',
                    )
    ordering = ('pk',)
    list_filter = ('model',)


admin.site.register(Bike, BikeAdmin)
admin.site.register(Owner)
admin.site.register(Ownership)
