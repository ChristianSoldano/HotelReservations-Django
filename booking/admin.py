from django.contrib import admin
from booking.models import *

class BookingAdmin(admin.ModelAdmin):
    list_display = ['combine_firstname_and_lastname', 'get_property_name', 'checkin', 'checkout']
    #search_fields = ('start', 'finish',)

    def get_property_name(self, obj):
        return obj.property.title

    def combine_firstname_and_lastname(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)

    get_property_name.short_description = 'Property'  # Renames column head
    combine_firstname_and_lastname.short_description = 'Host'  # Renames column head

    def get_queryset(self, request):
        queryset = BookingManager.get_queryset(self, request)
        return queryset

####################################################################################################

class BookingPeriodAdmin(admin.ModelAdmin):
    list_display = ['start', 'finish', 'get_property_name']
    search_fields = ('start', 'finish',)

    def get_property_name(self, obj):
        return obj.property.title

    get_property_name.short_description = 'Property'  # Renames column head

    def get_queryset(self, request):
        queryset = BookingPeriodManager.get_queryset(self, request)
        return queryset
####################################################################################################

class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'get_property_name']

    def get_property_name(self, obj):
        return obj.property.title

    get_property_name.short_description = 'Property'  # Renames column head

    def get_queryset(self, request):
        queryset = ImageManager.get_queryset(self, request)
        return queryset


####################################################################################################

class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
####################################################################################################

class PropertyAdmin(admin.ModelAdmin):
    # inlineList = [InlineBookingPeriod]
    list_display = ['title', 'get_city_name', 'address']
    search_fields = ('title',)

    def get_city_name(self, obj):
        return obj.city.name

    get_city_name.short_description = 'City'  # Renames column head
    #Using that queryset manager created before
    def get_queryset(self, request):
        queryset = PropertyManager.get_queryset(self, request)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'host':
            if not request.user.is_superuser:
                print(Host.objects.filter(username = request.user))
                kwargs ["queryset"] = Host.objects.filter(username = request.user)
                kwargs ["initial"] = kwargs["queryset"][0]
        return super(PropertyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

####################################################################################################

admin.site.register(Property, PropertyAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingPeriod, BookingPeriodAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Host)


