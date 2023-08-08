from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from website.forms import AppointmentForm
from website.models import Mikvah, MikvahCalendar, Slots, Appointment
from datetime import datetime, timedelta, time
from django.utils import timezone


def user_group_is_client(user):
    return user.groups.filter(name='Client').exists()


@user_passes_test(user_group_is_client)
def client_page_view(request):
    mikvahs = Mikvah.objects.all()
    context = {
        'mikvahs': mikvahs,
    }
    return render(request, 'website/client_page.html', context)


def new_appointment_view(request, mikvah_id):
    mikvah_id = Mikvah.objects.get(mikvah_id=mikvah_id)
    form = AppointmentForm()
    slots = []
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            weekly_day = date.strftime('%A')
            mikvah_calendar = MikvahCalendar.objects.filter(mikvah_id=mikvah_id, day=weekly_day).first()
            print(mikvah_calendar)

            next_opening_time = mikvah_calendar.opening_time
            while next_opening_time < mikvah_calendar.closing_time:
                start_slot = next_opening_time
                end_slot = get_next_time(start_slot, 15)
                next_opening_time = end_slot
                try:
                    slot = Slots(mikvah_calendar=mikvah_calendar, start_time=start_slot, end_time=end_slot)
                    slot.save()
                except:
                    pass
            mikvah_appointments = Appointment.objects.filter(mikvah_id=mikvah_id, date=date)
            print('appointments', mikvah_appointments)
            slots = Slots.objects.filter(mikvah_calendar=mikvah_calendar)

            for appointment in mikvah_appointments:
                slots = slots.exclude(start_time__gte=appointment.start, end_time__lte=appointment.end)

    context = {'form': form, 'slots': slots, 'mikvah_id': mikvah_id.mikvah_id}
    return render(request, 'website/new_appointment.html', context)


def get_next_time(current_time, time_slot):
    opening_time = time(current_time.hour, current_time.minute, current_time.second)
    opening_datetime = datetime.combine(datetime.today(), opening_time)
    next_opening_time = (opening_datetime + timedelta(minutes=time_slot)).time()
    return next_opening_time


def save_appointment_view(request, mikvah_id):
    mikvah_id = Mikvah.objects.get(mikvah_id=mikvah_id)
    user = request.user
    if request.method == 'POST':
        selected_slots = request.POST.getlist('slot')
        if len(selected_slots) >= 1 and len(selected_slots) <= 3:
            slots = Slots.objects.filter(pk__in=selected_slots)

            start_time = slots[0].start_time
            end_time = slots[len(slots) - 1].end_time

            selected_date_str = request.POST.get('selected_date')
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_date_weekly = selected_date.strftime('%A')

            mikvah_calendar = MikvahCalendar.objects.filter(mikvah_id=mikvah_id, day=selected_date_weekly).first()
            appointment = Appointment(start=start_time, end=end_time, date=selected_date, mikvah_id=mikvah_id, user=user, mikvah_calendar=mikvah_calendar)
            appointment.save()
            print(appointment)
            return redirect('website:my_appointments')
        else:
            return HttpResponse('Please choose a maximum of 3 slots')
    else:
        context = {'mikvah_id': mikvah_id}
        return redirect('website:save_appointment', context)


def get_time_format(time_str):
    if time_str.lower() == 'noon':
        time_apm = time(hour=12, minute=0).strftime("%I:%M %p")
        time_obj = datetime.strptime(time_apm, "%I:%M %p").time()
    elif len(time_str) == 6:
        time_apm = time(hour=int(time_str[0]), minute=0).strftime("%I:%M %p")
        time_obj = datetime.strptime(time_apm, "%I:%M %p").time()
    else:
        time_str_re = time_str.replace(".", "")
        time_obj = datetime.strptime(time_str_re, "%I:%M %p").time()
    return time_obj


def my_appointments_view(request):
    appointments = Appointment.objects.filter(user=request.user, date__gte=timezone.now().date()).order_by('-date')
    context = {
        'appointments': appointments,
    }
    return render(request, 'website/my_appointments.html', context)


def my_past_appointments_view(request):
    appointments = Appointment.objects.filter(user=request.user, date__lt=timezone.now().date())
    context = {
        'appointments': appointments,
    }
    return render(request, 'website/my_past_appointments.html', context)


def cancel_appointment_view(request):
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        appointment.canceled = True
        appointment.save()
        return redirect('website:my_appointments')
    else:
        return render(request, 'website/my_appointments.html')