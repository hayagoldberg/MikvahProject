from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.


class Mikvah(models.Model):
    mikvah_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone_nb1 = models.CharField(max_length=20)
    phone_nb2 = models.CharField(max_length=20, blank=True)
    open_at = models.TimeField(blank=True)
    ashkenaz = models.BooleanField(default=False)
    sefarad = models.BooleanField(default=False)
    chabad = models.BooleanField(default=False)
    address_nb = models.CharField(max_length=4)
    address_st = models.CharField(max_length=40)
    address_city = models.CharField(max_length=40)
    address_state = models.CharField(max_length=20)
    address_country = models.CharField(max_length=40)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    distance = models.FloatField(null=True, blank=True)

    def get_gps_link(self):
        # to be able to display a Google map link for each mikvah
        gps_link = f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return gps_link

# choice fields for MikvahCalendar
CHOICES_DAY = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
        )

class MikvahCalendar(models.Model):
    # opening time of the mikvah
    mikvah_id = models.ForeignKey(Mikvah, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=CHOICES_DAY)
    opening_time = models.TimeField(blank=True)
    closing_time = models.TimeField(blank=True)

    def calculate_opening_time_duration(self):
        # function to calculate the time that the mikvah will be open in minutes
        start_time = self.opening_time
        end_time = self.closing_time
        duration_minutes = (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute)
        return duration_minutes

    def __str__(self):
        return f"{self.day} from {self.opening_time} to {self.closing_time}"


class Slots(models.Model):
    # model to save the slots for creating new appointments
    mikvah_calendar = models.ForeignKey(MikvahCalendar, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('mikvah_calendar', 'start_time', 'end_time')


class Appointment(models.Model):
    # to save the appointments and connect them to yhe user and the mikvah
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    mikvah_id = models.ForeignKey(Mikvah, on_delete=models.CASCADE, blank=True)
    mikvah_calendar = models.ForeignKey(MikvahCalendar, on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    start = models.TimeField(blank=True)
    end = models.TimeField(blank=True)
    canceled = models.BooleanField(default=False)
