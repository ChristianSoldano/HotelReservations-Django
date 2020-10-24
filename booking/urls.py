from django.urls import path
from booking.views import *

urlpatterns = [
    path('', home_page, name='index'),
    path('list/', properties_list, name='property_list'),
    path('details/<int:id_property>', property_detail, name='property_details'),
]
