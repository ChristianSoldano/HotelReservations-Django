from django.urls import path
from booking.views import *

urlpatterns = [
    path('', home_page, name='index'),
    path('list/', property_list, name='property_list'),
    path('details/', property_details, name='property_details'),
    path('formulario/', formulario, name='formulario'),
]
