from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Now


class Host(User):
    dni = models.CharField(max_length=8, unique=True)

    class Meta:
        verbose_name_plural = "Hosts"
        verbose_name = "Host"


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        verbose_name_plural = "Cities"
        verbose_name = "City"


class Property(models.Model):
    # si explota hay que ver el on_delete de aca abajo. Cambia el ondelete por models.PROTECTED
    host = models.ForeignKey(Host, on_delete=models.PROTECT, blank=False, null=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    rate = models.FloatField(null=False, blank=False)
    pax = models.IntegerField(null=False, blank=False)
    rooms = models.IntegerField(null=False, blank=False)
    bathrooms = models.IntegerField(null=False, blank=False)
    beds = models.IntegerField(null=False, blank=False)
    garage = models.IntegerField(null=False, blank=False)
    pets = models.BooleanField(null=False, blank=False)
    wifi = models.BooleanField(null=False, blank=False)
    pool = models.BooleanField(null=False, blank=False)
    kitchen = models.BooleanField(null=False, blank=False)
    active = models.BooleanField(default=True, null=False)

    class Meta:
        verbose_name_plural = "Properties"
        verbose_name = "Property"


class Image(models.Model):
    image = models.ImageField(null=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Images"
        verbose_name = "Image"


class Booking(models.Model):
    first_name = models.CharField(blank=False, null=False, max_length=50)
    last_name = models.CharField(blank=False, null=False, max_length=50)
    email = models.EmailField(blank=False, null=False, max_length=200)
    # si explota hay que ver el on_delete de aca abajo. Cambia el ondelete por models.PROTECTED
    property = models.ForeignKey(Property, on_delete=models.PROTECT, blank=False, null=False)
    checkin = models.DateField(blank=False, null=False)
    checkout = models.DateField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Bookings"
        verbose_name = "Booking"


class BookingPeriod(models.Model):
    start = models.DateField(blank=False, null=False)
    finish = models.DateField(blank=False, null=False)
    property = models.ForeignKey(Property, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # TODO checkear que la fecha del nuevo periodo a cargar sea mayor a la de cierre del ultimo periodo
            #  y que sea mayor a hoy
            models.CheckConstraint(
                name="finish_date_constraint",
                check=(models.Q(finish__gt=models.F("start") and Now()))
            ),
            models.UniqueConstraint(
                name="unique_date_constraint",
                fields=['start', 'finish', 'property']
            )]
        verbose_name_plural = "Booking Periods"
        verbose_name = "Booking Period"
