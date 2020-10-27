from django.shortcuts import render, redirect
from booking.models import *
from dateutil.parser import parse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group


def home_page(request):
    cities = []
    cities = City.objects.all()
    return render(request, 'index.html',{'cities': cities})

def properties_list(request):
    cities = []
    properties = []
    booking_periods = []
    property_filters = {
        "active": True
    }

    if request.method == 'POST':

        for key in request.POST:
            if key != 'csrfmiddlewaretoken' and key != 'priceRange' and key != "datePickCheckout" and key != "datePickCheckin":
                if request.POST[key] != "any":
                    if request.POST[key] == 'true':
                        property_filters[key] = True
                    else:
                        property_filters[key + "__gte"] = int(request.POST[key])
                    if key == "city":
                            property_filters[key] = City.objects.filter(id=request.POST[key])[0]

        price = request.POST["priceRange"].split("-")

        property_filters["rate__gte"] = price[0]
        property_filters["rate__lte"] = price[1]

        if request.POST['datePickCheckin'] != "":
            booking_periods = BookingPeriod.objects.filter(start__lte=parse(request.POST['datePickCheckin']), finish__gte=parse(request.POST['datePickCheckout']))
            for period in booking_periods:
                v = Property.objects.filter(**property_filters)
                for v_property in v:
                    if period.property == v_property:
                        properties.append(v_property)
        else:
            properties = Property.objects.filter(**property_filters)

    print(properties)
    cities = City.objects.all()


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


def register_view(request):
    return render(request, "register.html")


def register(request):
    if request.method == 'POST':
        # user = User.objects.create_user().save()

        host = Host(email=request.POST["email"],
                    username=request.POST["username"],
                    first_name=request.POST["firstname"],
                    last_name=request.POST["lastname"],
                    dni=request.POST["dni"],
                    is_staff=1,
                    )
        host.set_password(request.POST["password"])
        host.save()

        group = Group.objects.get(name='Host')
        host.groups.add(group)

        login_data = authenticate(username=request.POST["username"], password=request.POST["password"])
        login(request, login_data)
    return redirect("admin:index")
