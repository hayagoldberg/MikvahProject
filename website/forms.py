from django import forms
from django.forms import ModelForm
from .models import Mikvah, MikvahCalendar


class MikvahSearchFormCF(forms.Form):
    search_name = forms.CharField(label='Search by name', max_length=100, required=False)
    search_city = forms.CharField(label='Search by city', max_length=100, required=False)


class MikvahSearchFormGPS(forms.Form):
    search_longitude = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    search_latitude = forms.DecimalField(widget=forms.HiddenInput(), required=False)


class MikvahForm(ModelForm):
    class Meta:
        model = Mikvah
        fields = ('name', 'phone_nb1', 'phone_nb2', 'open_at', 'ashkenaz', 'sefarad', 'chabad',
                  'address_nb', 'address_st', 'address_city', 'address_state', 'address_country',
                  'longitude', 'latitude', )
        labels = {
            'name': 'Name of the Mikvah',
            'phone_nb1': 'Phone number',
            'phone_nb2': 'Mobile number',
            'address_nb': 'Street address',
            'address_st': 'Street address line 2',
            'address_city': 'City',
            'address_state': 'State/Province',
            'longitude': 'GPS position, longitude',
            'latitude': 'GPS position latitude'
        }
        required = {
            'phone_nb2': False,
            'address_st': False,
            'address_state': False,
        }


class CalendarForm(ModelForm):
    class Meta:
        model = MikvahCalendar
        fields = ('mikvah_id', 'day', 'opening_time', 'closing_time')
        labels = {'mikvah_id': 'mikvah ID', 'day': 'Day of the week', 'opening_time': 'Opening time', 'closing_time': 'Closing time'}


class AppointmentForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
