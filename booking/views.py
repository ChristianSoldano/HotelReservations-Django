from booking.models import Property, City, Booking
from django.shortcuts import render, redirect


# Create your views here.

def home_page(request):
    return render(request, 'index.html')


def properties_list(request):
    cities = City.objects.all()
    properties = Property.objects.all()

    return render(request, 'properties-list.html', {'properties': properties, 'cities': cities})


def property_detail(request, id_property):
    obj = Property.objects.get(id=id_property)
    return render(request, 'properties-detail.html', {'property': obj})


def do_a_booking(request):
    booking = Booking(
        property=Property.objects.get(id=request.POST['idProperty']),
        checkin=request.POST['checkin'],
        checkout=request.POST['checkout'],
        email=request.POST['email'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'])
    booking.save()
    return redirect('booking:properties_list', request)  # No se si va
