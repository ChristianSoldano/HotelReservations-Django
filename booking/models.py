from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Now

class PropertyManager(models.Manager):
    def get_queryset(self, request):
        query = Property.objects.filter(host=request.user)
        if request.user.is_superuser:
            query = Property.objects.all()
        return query

class Host(User):
    dni = models.CharField(max_length=8, unique=True)
    created_at = models.DateField(auto_now=True, blank=False, null=False)
    updated_at = models.DateField(auto_now=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Hosts"
        verbose_name = "Host"


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    created_at = models.DateField(auto_now=True, blank=False, null=False)
    updated_at = models.DateField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"
        verbose_name = "City"


class Property(models.Model):
    host = models.ForeignKey(Host, on_delete=models.PROTECT, blank=False, null=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=50, null=True, blank=False)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    description = models.TextField(null=False, blank=False)
    rate = models.FloatField(null=False, blank=False)
    pax = models.IntegerField(null=False, blank=False)
    rooms = models.IntegerField(null=False, blank=False)
    bathrooms = models.IntegerField(null=False, blank=False)
    beds = models.IntegerField(null=False, blank=False)
    garage = models.BooleanField(null=False, blank=False)
    pets = models.BooleanField(null=False, blank=False)
    wifi = models.BooleanField(null=False, blank=False)
    pool = models.BooleanField(null=False, blank=False)
    kitchen = models.BooleanField(null=False, blank=False)
    active = models.BooleanField(default=True, null=False)
    created_at = models.DateField(auto_now=True, blank=False, null=False)
    updated_at = models.DateField(auto_now=True, blank=False, null=False)
    thumbnail = models.ImageField(null=False, upload_to="booking/static/img/properties",
                                  default="img/image-not-found.png")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Properties"
        verbose_name = "Property"


class Image(models.Model):
    image = models.ImageField(null=False, upload_to="booking/static/img/properties")
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Images"
        verbose_name = "Image"


class Booking(models.Model):
    first_name = models.CharField(blank=False, null=False, max_length=50)
    last_name = models.CharField(blank=False, null=False, max_length=50)
    email = models.EmailField(blank=False, null=False, max_length=200)
    property = models.ForeignKey(Property, on_delete=models.PROTECT, blank=False, null=False)
    checkin = models.DateField(blank=False, null=False)
    checkout = models.DateField(blank=False, null=False)
    created_at = models.DateField(auto_now=True, blank=False, null=False)
    updated_at = models.DateField(auto_now=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Bookings"
        verbose_name = "Booking"


class BookingPeriod(models.Model):
    start = models.DateField(blank=False, null=False)
    finish = models.DateField(blank=False, null=False)
    property = models.ForeignKey(Property, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True, blank=False, null=False)
    updated_at = models.DateField(auto_now=True, blank=False, null=False)

    class Meta:
        constraints = [
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
