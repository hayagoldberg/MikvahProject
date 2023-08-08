from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from website.forms import MikvahSearchFormGPS, MikvahSearchFormCF
from website.models import Mikvah
import decimal
from geopy.distance import distance

# views.py


def index_view(request):
    # Handle GET requests for search forms
    if request.method == "GET":
        # Initialize CF (city and name) and GPS search forms
        search_form_cf = MikvahSearchFormCF(request.GET)
        search_form_gps = MikvahSearchFormGPS(request.GET)

        # If CF search form is valid, perform a redirect
        if search_form_cf.is_valid():
            # Extract cleaned data and build query parameters
            search_name = search_form_cf.cleaned_data['search_name']
            search_city = search_form_cf.cleaned_data['search_city']
            query_params = {}
            if search_name:
                query_params['search_name'] = search_name
            if search_city:
                query_params['search_city'] = search_city

            # Redirect to 'search_result' view with query parameters
            if query_params:
                return redirect(reverse('website:search_result') + '?' + urlencode(query_params))

        # If GPS search form is valid, perform a redirect
        elif search_form_gps.is_valid():
            # Extract cleaned data and build query parameters
            search_longitude = search_form_gps.cleaned_data['search_longitude']
            search_latitude = search_form_gps.cleaned_data['search_latitude']
            if search_longitude and search_latitude:
                query_params = {'search_longitude': search_longitude, 'search_latitude': search_latitude}
                return redirect(reverse('website:search_result') + '?' + urlencode(query_params))
    else:
        # If the request method is not GET, create empty search forms
        search_form_cf = MikvahSearchFormCF()
        search_form_gps = MikvahSearchFormGPS()

    # Prepare the context with the search forms and the user
    context = {
        'search_form_cf': search_form_cf,
        'search_form_gps': search_form_gps,
        'user': request.user
    }
    # Render the 'index.html' template with the context
    return render(request, 'website/index.html', context)

def search_result_view(request):
    # Get the search parameters from the request's GET data
    search_name = request.GET.get('search_name')
    search_city = request.GET.get('search_city')
    search_longitude = request.GET.get('search_longitude')
    search_latitude = request.GET.get('search_latitude')

    # If name or city search parameters are provided
    if search_name or search_city:
        # Perform a filter on Mikvah model based on the provided parameters
        search_results = Mikvah.objects.filter(name__icontains=search_name, address_city__icontains=search_city)
    else:
        # If no name or city provided, set search_results to a placeholder value ('jjj')
        search_results = 'jjj'

    # If longitude and latitude search parameters are provided
    if search_longitude is not None and search_latitude is not None:
        # Get all Mikvah objects and calculate their distance from user's coordinates
        search_results = Mikvah.objects.all()
        for mikvah in search_results:
            mikvah_latitude = decimal.Decimal(mikvah.latitude)
            mikvah_longitude = decimal.Decimal(mikvah.longitude)
            mikvah_coordinates = (mikvah_latitude, mikvah_longitude)
            user_coordinates = (search_latitude, search_longitude)
            dist = distance(user_coordinates, mikvah_coordinates).km
            mikvah.distance = dist
        # Sort the Mikvah objects based on the calculated distance
        search_results = sorted(search_results, key=lambda mikvah: mikvah.distance)

    # Prepare the context with the search results
    context = {'mikvahs': search_results}
    # Render the 'search_result.html' template with the context
    return render(request, 'website/search_result.html', context)


def test_view(request):
    return HttpResponse("just a test view to see of changes are saved correctly on git")