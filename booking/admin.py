from django.contrib import admin
from booking.models import *


class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Host)
admin.site.register(Property, PropertyAdmin)
admin.site.register(City)
admin.site.register(Image)
admin.site.register(Booking)
admin.site.register(BookingPeriod)
