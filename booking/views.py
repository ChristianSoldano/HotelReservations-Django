from django.shortcuts import render, redirect
from booking.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
import datetime
from django.db.models import Q
import pandas
from django.urls import reverse
from urllib.parse import urlencode
from django.core.paginator import Paginator


def home_page(request):
    cities = City.objects.all()
    if "booking_id" and "property_title" and "checkin" and "checkout" and "name" and "total" in request.GET:
        booking_id = request.GET.get('booking_id')
        property_title = request.GET.get('property_title')
        checkin = datetime.datetime.strptime(request.GET.get('checkin'), '%Y-%m-%d').strftime('%d-%m-%Y')
        checkout = datetime.datetime.strptime(request.GET.get('checkout'), '%Y-%m-%d').strftime('%d-%m-%Y')
        name = request.GET.get('name')
        total = request.GET.get('total')
        params = {'booking_id': booking_id,
                  "property_title": property_title,
                  "checkin": checkin,
                  "checkout": checkout,
                  "name": name,
                  "total": total}
        return render(request, 'index.html', {'cities': cities, 'params': params})
    else:
        return render(request, 'index.html', {'cities': cities})


def properties_list(request):
    cities = []
    properties = []
    booking_periods = []
    property_filters = {
        "active": True
    }
    allowed_parameters = ["pax", "rooms", "bathrooms", "beds", "city", "garage", "pets", "wifi", "pool", "kitchen"]
    if request.method == 'GET':
        for key in request.GET:
            if key in allowed_parameters:
                if request.GET[key] != "any":
                    if request.GET[key] == 'true':
                        property_filters[key] = True
                    else:
                        property_filters[key + "__gte"] = int(request.GET[key])
                    if key == "city":
                        property_filters[key] = City.objects.filter(id=request.GET[key])[0]
        if "priceRange" in request.GET:
            price = request.GET["priceRange"].split("-")
            property_filters["rate__gte"] = price[0]
            property_filters["rate__lte"] = price[1]

        if "datePickCheckin" in request.GET and request.GET['datePickCheckin'] != "":
            booking_periods = BookingPeriod.objects.filter(
                start__lte=datetime.datetime.strptime(request.GET['datePickCheckin'], '%d-%m-%Y').date(),
                finish__gte=datetime.datetime.strptime(request.GET['datePickCheckout'], '%d-%m-%Y').date())
            for period in booking_periods:
                checkin = datetime.datetime.strptime(request.GET['datePickCheckin'], '%d-%m-%Y').date()
                checkout = datetime.datetime.strptime(request.GET['datePickCheckout'], '%d-%m-%Y').date()

                if not Booking.objects.filter(
                        Q(checkin__range=(checkin, checkout)) | Q(checkout__range=(checkin, checkout))).exists():
                    v = Property.objects.filter(**property_filters)
                    for v_property in v:
                        if period.property == v_property:
                            properties.append(v_property)
        else:
            properties = Property.objects.filter(**property_filters)
    else:
        properties = Property.objects.filter(**property_filters)

    cities = City.objects.all()

    for p in properties:
        p.thumbnail = (str(p.thumbnail).replace("booking/static/", ""))

    paginator = Paginator(properties, 5)
    page = request.GET.get('page')
    properties = paginator.get_page(page)

    if request.method == 'GET':
        url_params = request.GET.copy()
        final_url = "?"
        for p in url_params:
            if p != "page":
                final_url += p + "=" + url_params[p] + "&"

    return render(request, 'property-list.html', {'properties': properties, 'cities': cities, 'final_url': final_url})


def property_detail(request, id_property):
    v_property = Property.objects.get(id=id_property)
    images = Image.objects.filter(property__id=id_property)
    # format dd-mm-yyyy
    available_dates = []
    reserved_dates = []
    final_dates = []

    periods = BookingPeriod.objects.filter(property=v_property)
    reserved_periods = Booking.objects.filter(property=v_property)

    for period in periods:
        available_dates += pandas.date_range(start=period.start, end=period.finish, freq='d')

    for rd in reserved_periods:
        reserved_dates += pandas.date_range(start=rd.checkin, end=rd.checkout, freq='d')

    available_dates = list(set(available_dates) - set(reserved_dates))

    available_dates.sort()

    for d in available_dates:
        final_dates.append(datetime.datetime.strptime(str(d.date()), '%Y-%m-%d').strftime('%#d-%m-%Y'))

    v_property.thumbnail = (str(v_property.thumbnail).replace("booking/static/", ""))

    for image in images:
        image.image = (str(image.image).replace("booking/static/", ""))

    return render(request, 'property-details.html',
                  {'property': v_property, 'reserved_dates': final_dates, 'images': images})


def do_a_booking(request):
    if request.method == 'POST':
        if "idProperty" and "firstname" and "lastname" and "email" and "datePickCheckin" and "datePickCheckout" and \
                "totalDays" in request.POST:
            print(request.POST["totalDays"])
            property_to_rent = Property.objects.get(id=request.POST['idProperty'])
            start_date = datetime.datetime.strptime(request.POST['datePickCheckin'], '%d-%m-%Y').date()
            finish_date = datetime.datetime.strptime(request.POST['datePickCheckout'], '%d-%m-%Y').date()

            if not Booking.objects.filter(checkin__range=(start_date, finish_date),
                                          checkout__range=(start_date, finish_date)).exists():
                booking = Booking(
                    property=property_to_rent,
                    checkin=start_date,
                    checkout=finish_date,
                    email=request.POST['email'],
                    first_name=request.POST['firstname'],
                    last_name=request.POST['lastname'],
                    total=property_to_rent.rate * float(request.POST["totalDays"]) * 1.08)
                booking.save()

            base_url = reverse('index')

            query_string = urlencode({'booking_id': booking.id,
                                      "property_title": property_to_rent.title,
                                      "checkin": booking.checkin,
                                      "checkout": booking.checkout,
                                      "name": booking.first_name + " " + booking.last_name,
                                      "total": booking.total})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        else:
            return redirect("index")
    else:
        return redirect("index")


def register_view(request):
    return render(request, "register.html")


def register(request):
    if request.method == 'POST':
        if "email" and "username" and "password" and "firstname" and "lastname" and "dni" in request.POST:
            errors = []
            if User.objects.filter(email=request.POST["email"]).exists():
                errors.append("The email is already in use")

            if User.objects.filter(username=request.POST["username"]).exists():
                errors.append("The username is already in use")

            if Host.objects.filter(dni=request.POST["dni"]).exists():
                errors.append("The dni is already in use")

            if errors:
                return render(request, "register.html", {"errors": errors})

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
        else:
            return redirect("index")
    else:
        return redirect("index")
