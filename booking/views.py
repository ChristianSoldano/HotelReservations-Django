from django.shortcuts import render, redirect
from booking.models import *


def home_page(request):
    return render(request, 'index.html')


def properties_list(request):
    cities = []
    properties = []

    property_filters = {
        "active": True
    }

    if request.method == 'POST':

        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and key != 'priceRange':
                if request.POST[key] != "any":
                    property_filters[key] = int(request.POST[key])

        # if request.POST["pax"] != "any":
        #     property_filters["pax"] = int(request.POST["pax"])
        # if request.POST["rooms"] != "any":
        #     property_filters["rooms"] = int(request.POST["rooms"])
        # if request.POST["bathrooms"] != "any":
        #     property_filters["bathrooms"] = int(request.POST["bathrooms"])
        # if request.POST["beds"] != "any":
        #     property_filters["beds"] = int(request.POST["beds"])

        price = request.POST["priceRange"].split("-")

        property_filters["rate__gte"] = price[0]
        property_filters["rate__lte"] = price[1]

        properties = Property.objects.filter(**property_filters)
    else:
        cities = City.objects.all()
        properties = Property.objects.filter(**property_filters)

    return render(request, 'property-list.html', {'properties': properties, 'cities': cities})


def property_detail(request, id_property):
    obj = Property.objects.get(id=id_property)
    # format dd-mm-yyyy
    reserved_dates = ["24-10-2020", "25-10-2020", "28-10-2020", "29-10-2020", "30-10-2020"]
    return render(request, 'property-details.html', {'property': obj, 'reserved_dates': reserved_dates})


def do_a_booking(request):
    property_to_rent = Property.objects.get(id=request.POST['idProperty'])
    period = BookingPeriod.objects.filter(start__lte=request.POST['checkin'],
                                          finish__gte=request.POST['checkout'], property=property_to_rent)
    # Testear y ver de usar el distinct en caso de que el exclude no sirva
    if Booking.objects.filter(checkin__range=(period.start, period.finish),
                              checkout__range=(period.start, period.finish)).exists():
        print("No se puede hacer la reserva")
    else:
        booking = Booking(
            property=property_to_rent,
            checkin=request.POST['checkin'],
            checkout=request.POST['checkout'],
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'])
        booking.save()

    return redirect('booking:properties_list', request)  # No se si va


def register(request):
    return render(request, 'register.html')
