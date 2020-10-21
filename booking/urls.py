from django.urls import path
from booking.views import *

urlpatterns = [
    path('', home_page, name='index')
]
