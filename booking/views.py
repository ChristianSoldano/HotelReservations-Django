from django.shortcuts import render
from booking.models import *


def home_page(request):
    return render(request, 'index.html')


def property_list(request):
    city = City("Mar del Plata")
    host = Host()
    p1 = Property()

    p1.title = "Cabaña hermosa"
    p1.description = "Loreim mipsd psad ñlkasd ñlskd wod w3ofk wogj rgi jtrgh lkfg"
    p1.rate = 3000
    p1.pax = 5
    p1.rooms = 6
    p1.bathrooms = 8
    p1.beds = 7
    p1.garage = True
    p1.pets = True
    p1.wifi = True
    p1.pool = True
    p1.kitchen = True
    p1.active = True


    properties = [p1]

    print(p1.title)
    print(p1.description)
    print(p1.rate)
    print(p1.pax)
    print(p1.rooms)
    print(p1.bathrooms)
    print(p1.beds)
    print(p1.garage)
    print(p1.pets)
    print(p1.wifi)
    print(p1.pool)
    print(p1.kitchen)
    print(p1.active)
    return render(request, 'property-list.html', {"properties": properties})


def property_details(request):
    return render(request, 'property-details.html')


def formulario(request):
    paxs = request.POST.get('paxs')
    rooms = request.POST.get('rooms')
    bathrooms = request.POST.get('bathrooms')
    beds = request.POST.get('beds')
    garage = request.POST.get('garage')
    pets = request.POST.get('pets')
    wifi = request.POST.get('wifi')
    pool = request.POST.get('pool')
    kitchen = request.POST.get('kitchen')
    price_range = request.POST.get('priceRange')

    print("paxs: ", paxs)
    print("rooms: ", rooms)
    print("bathrooms: ", bathrooms)
    print("beds: ", beds)
    print("garage: ", garage)
    print("pets: ", pets)
    print("wifi: ", wifi)
    print("pool: ", pool)
    print("kitchen: ", kitchen)
    print("price_range: ", price_range)

    return render(request, 'formulario.html')
