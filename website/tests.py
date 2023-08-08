# from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth.decorators import user_passes_test
# from django.urls import reverse
# from django.db.models import Q
# from urllib.parse import urlencode
# from .forms import MikvahForm, MikvahSearchFormGPS, MikvahSearchFormCF, AppointmentForm, AvailableDateForm, AppointmentForm2
# from .models import Mikvah, MikvahCalendar, CHOICES_DAY, Appointment, Slots, Appointment2, Appointment3
# import decimal
# from geopy.distance import distance
# from datetime import datetime, timedelta, time
# from django.utils import timezone
#
#
# # Create your views here.
# def index_view(request):
#     if request.method == "GET":
#         search_form_cf = MikvahSearchFormCF(request.GET)
#         search_form_gps = MikvahSearchFormGPS(request.GET)
#
#         if search_form_cf.is_valid():
#             search_name = search_form_cf.cleaned_data['search_name']
#             search_city = search_form_cf.cleaned_data['search_city']
#             query_params = {}
#             if search_name:
#                 query_params['search_name'] = search_name
#             if search_city:
#                 query_params['search_city'] = search_city
#             if query_params:
#                 return redirect(reverse('website:search_result') + '?' + urlencode(query_params))
#
#         elif search_form_gps.is_valid():
#             search_longitude = search_form_gps.cleaned_data['search_longitude']
#             search_latitude = search_form_gps.cleaned_data['search_latitude']
#             if search_longitude and search_latitude:
#                 query_params = {'search_longitude': search_longitude,
#                                 'search_latitude': search_latitude}
#                 return redirect(reverse('website:search_result') + '?' + urlencode(query_params))
#     else:
#         search_form_cf = MikvahSearchFormCF()
#         search_form_gps = MikvahSearchFormGPS()
#
#     context = {
#         'search_form_cf': search_form_cf,
#         'search_form_gps': search_form_gps,
#         'user': request.user
#     }
#     return render(request, 'website/index.html', context)
#
#
# def search_result_view(request):
#     search_name = request.GET.get('search_name')
#     search_city = request.GET.get('search_city')
#     search_longitude = request.GET.get('search_longitude')
#     search_latitude = request.GET.get('search_latitude')
#
#     if search_name or search_city:
#         search_results = Mikvah.objects.filter(name__icontains=search_name, address_city__icontains=search_city,)
#     else:
#         search_results = 'jjj'
#
#     if search_longitude is not None and search_latitude is not None:
#
#         search_results = Mikvah.objects.all()
#         for mikvah in search_results:
#             mikvah_latitude = decimal.Decimal(mikvah.latitude)
#             mikvah_longitude = decimal.Decimal(mikvah.longitude)
#             mikvah_coordinates = (mikvah_latitude, mikvah_longitude)
#             user_coordinates = (search_latitude, search_longitude)
#             dist = distance(user_coordinates, mikvah_coordinates).km
#             mikvah.distance = dist
#         search_results = sorted(search_results, key=lambda mikvah: mikvah.distance)
#
#     context = {'mikvahs': search_results}
#     return render(request, 'website/search_result.html', context)
#
#
# def my_mikvah(request):
#     if request.method == 'POST':
#         if 'mikvah-calendar' in request.POST:
#             return redirect('website:mikvah_calendar')
#     else:
#         user = request.user
#         my_mikvahs = Mikvah.objects.filter(user=user)
#         mikvah_ids = my_mikvahs.values_list('mikvah_id', flat=True)
#         my_mikvah_calendars = MikvahCalendar.objects.all()
#     context = {'mikvahs': my_mikvahs,
#                'mikvah_calendars': my_mikvah_calendars, }
#     return render(request, 'website/my_mikvah.html', context)
#
#
# def add_mikvah(request):
#     if request.method == "POST":
#         form = MikvahForm(request.POST)
#         if form.is_valid():
#             mikvah = form.save(commit=False)
#             mikvah.user = request.user
#             mikvah.save()
#             return redirect('website:my_mikvah')
#     else:
#         form = MikvahForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'website/add_mikvah.html', context)
#
#
# def user_group_is_professional(user):
#     return user.groups.filter(name='Professional').exists()
#
#
# @user_passes_test(user_group_is_professional)
# def pro_page_view(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             if 'my-mikvah' in request.POST:
#                 return redirect('website:my_mikvah')
#             elif 'add-mikvah' in request.POST:
#                 return redirect('website:add_mikvah')
#         return render(request, 'website/pro_page.html')
#     else:
#         return redirect('website:index')
#
#
# def user_group_is_client(user):
#     return user.groups.filter(name='Client').exists()
#
#
# @user_passes_test(user_group_is_client)
# def client_page_view(request):
#     mikvahs = Mikvah.objects.all()
#     context = {
#         'mikvahs': mikvahs,
#     }
#     return render(request, 'website/client_page.html', context)
#
#
# @user_passes_test(user_group_is_professional)
# def mikvah_calendar_view(request, mikvah_id):
#     days_of_week = CHOICES_DAY
#     if request.method == "POST":
#         mikvah = Mikvah.objects.get(mikvah_id=mikvah_id)
#         for i in range(1, 8):
#             day = request.POST.get(f"day_{i}")
#             opening_time = request.POST.get(f"opening_time_{i}")
#             closing_time = request.POST.get(f"closing_time_{i}")
#             mikvah_calendar = MikvahCalendar(
#                 day=day,
#                 opening_time=opening_time,
#                 closing_time=closing_time,
#                 mikvah_id=mikvah,
#             )
#             mikvah_calendar.save()
#             return redirect('website:my_mikvah')
#
#     context = {
#         'days_of_week': days_of_week,
#         }
#     return render(request, 'website/mikvah_calendar.html', context)
#
#
# def add_minutes(time_obj, minutes):
#     hours, mins = divmod(time_obj.hour * 60 + time_obj.minute + minutes, 60)
#     return time(hours, mins)
#
#
# def new_appointment_view2(request, mikvah_id):
#     mikvah_id = Mikvah.objects.get(mikvah_id=mikvah_id)
#     form = AppointmentForm2()
#     slots = []
#     if request.method == "POST":
#         form = AppointmentForm2(request.POST)
#         if form.is_valid():
#             date = form.cleaned_data['date']
#             weekly_day = date.strftime('%A')
#             mikvah_calendar = MikvahCalendar.objects.filter(mikvah_id=mikvah_id, day=weekly_day).first()
#             print(mikvah_calendar)
#
#             next_opening_time = mikvah_calendar.opening_time
#             while next_opening_time < mikvah_calendar.closing_time:
#                 start_slot = next_opening_time
#                 end_slot = get_next_time(start_slot, 15)
#                 next_opening_time = end_slot
#                 try:
#                     slot = Slots(mikvah_calendar=mikvah_calendar, start_time=start_slot, end_time=end_slot)
#                     slot.save()
#                 except:
#                     pass
#             mikvah_appointments = Appointment3.objects.filter(mikvah_id=mikvah_id, date=date)
#             print('appointments', mikvah_appointments)
#             slots = Slots.objects.filter(mikvah_calendar=mikvah_calendar)
#
#             for appointment in mikvah_appointments:
#                 slots = slots.exclude(start_time__gte=appointment.start, end_time__lte=appointment.end)
#
#     context = {'form': form, 'slots': slots, 'mikvah_id': mikvah_id.mikvah_id}
#     return render(request, 'website/new_appointment2.html', context)
#
#
# def get_next_time(current_time, time_slot):
#     opening_time = time(current_time.hour, current_time.minute, current_time.second)
#     opening_datetime = datetime.combine(datetime.today(), opening_time)
#     next_opening_time = (opening_datetime + timedelta(minutes=time_slot)).time()
#     return next_opening_time
#
#
# def save_appointment_view(request, mikvah_id):
#     mikvah_id = Mikvah.objects.get(mikvah_id=mikvah_id)
#     user = request.user
#     if request.method == 'POST':
#         selected_slots = request.POST.getlist('slot')
#         if len(selected_slots) >= 1 and len(selected_slots) <= 3:
#             slots = Slots.objects.filter(pk__in=selected_slots)
#
#             start_time = slots[0].start_time
#             end_time = slots[len(slots) - 1].end_time
#
#             selected_date_str = request.POST.get('selected_date')
#             selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
#             selected_date_weekly = selected_date.strftime('%A')
#
#             mikvah_calendar = MikvahCalendar.objects.filter(mikvah_id=mikvah_id, day=selected_date_weekly).first()
#             appointment = Appointment3(start=start_time, end=end_time, date=selected_date, mikvah_id=mikvah_id, user=user, mikvah_calendar=mikvah_calendar)
#             appointment.save()
#             print(appointment)
#             return redirect('website:my_appointments')
#         else:
#             return HttpResponse('Please choose a maximum of 3 slots')
#     else:
#         context = {'mikvah_id': mikvah_id}
#         return redirect('website:save_appointment', context)
#
#
# def get_time_format(time_str):
#     if time_str.lower() == 'noon':
#         time_apm = time(hour=12, minute=0).strftime("%I:%M %p")
#         time_obj = datetime.strptime(time_apm, "%I:%M %p").time()
#     elif len(time_str) == 6:
#         time_apm = time(hour=int(time_str[0]), minute=0).strftime("%I:%M %p")
#         time_obj = datetime.strptime(time_apm, "%I:%M %p").time()
#     else:
#         time_str_re = time_str.replace(".", "")
#         time_obj = datetime.strptime(time_str_re, "%I:%M %p").time()
#     return time_obj
#
#
# def new_appointment_view(request, mikvah_id):
#     if request.method == "POST":
#         mikvah = Mikvah.objects.get(mikvah_id=mikvah_id)
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             date = form.cleaned_data['date']
#             beginning_time = form.cleaned_data['beginning_time']
#             ending_time = appointment.calculate_end_time()
#
#             day = date.strftime('%A')
#             print(date, date.strftime('%A'), beginning_time, ending_time)
#
#             mikvah_calendar = MikvahCalendar.objects.filter(mikvah_id=mikvah_id, day=day,
#                                                             opening_time__lte=beginning_time,
#                                                             closing_time__gte=ending_time)
#             if not mikvah_calendar:
#                 return HttpResponse('Le mikvah est fermé à cette heure-ci')
#
#             if Appointment.objects.filter(Q(mikvah_id=mikvah_id, date=date) &
#                                           Q(Q(beginning_time__lte=ending_time, ending_time__gt=ending_time) |
#                                             Q(beginning_time__lt=beginning_time, ending_time__gte=beginning_time))).exists():
#                 return HttpResponse('Cette heure est déjà réservée. Veuillez choisir une autre heure')
#
#             else:
#                 appointment.mikvah_id = mikvah
#                 appointment.user = request.user
#                 appointment.ending_time = ending_time
#                 appointment.save()
#                 return redirect('website:my_appointments')
#     else:
#         form = AppointmentForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'website/new_appointment.html', context)
#
#
# def my_appointments_view(request):
#     appointments = Appointment3.objects.filter(user=request.user, date__gte=timezone.now().date())
#     context = {
#         'appointments': appointments,
#     }
#     return render(request, 'website/my_appointments.html', context)
#
#
# def my_past_appointments_view(request):
#     appointments = Appointment3.objects.filter(user=request.user, date__lt=timezone.now().date())
#     context = {
#         'appointments': appointments,
#     }
#     return render(request, 'website/my_past_appointments.html', context)
#
#
# def cancel_appointment_view(request):
#     if request.method == "POST":
#         appointment_id = request.POST.get('appointment_id')
#         appointment = Appointment3.objects.get(id=appointment_id, user=request.user)
#         appointment.canceled = True
#         appointment.save()
#         return redirect('website:my_appointments')
#     else:
#         return render(request, 'website/my_appointments.html')
#
#
# def mikvah_appointments_view(request, mikvah_id):
#     mikvah = Mikvah.objects.get(mikvah_id=mikvah_id)
#     appointments = Appointment3.objects.filter(mikvah_id=mikvah)
#     context = {
#        'appointments': appointments,
#        'mikvah_id': mikvah_id
#     }
#     return render(request, 'website/mikvah_appointments.html', context)
#
