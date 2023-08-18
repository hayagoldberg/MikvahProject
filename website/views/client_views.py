from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from website.forms import AppointmentForm
from website.models import Mikvah, MikvahCalendar, Slots, Appointment
from website.utils import user_group_is_client, get_next_time, get_time_format
from datetime import datetime
from django.utils import timezone


@user_passes_test(user_group_is_client)
def client_page_view(request):
    # View for the clients users only that displays a list of all the mikvah.
    mikvahs = Mikvah.objects.all()
    context = {
        'mikvahs': mikvahs,
    }
    return render(request, 'website/client_page.html', context)


def new_appointment_view(request, mikvah_id):
    # View to handle new appointment creation
    mikvah_id = Mikvah.objects.get(mikvah_id=mikvah_id)
    form = AppointmentForm()
    slots = []
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Get the date from the form, extract the day of the week and get the opening calendar of the mikvah for that day
            date = form.cleaned_data['date']
            weekly_day = date.strftime('%A')
            mikvah_calendar = MikvahCalendar.objects.filter(mikvah_id=mikvah_id, day=weekly_day).first()
            print(mikvah_calendar)

            # Creating time slots by using the 'get_next_time' function.
            # Repeat the process until closing time of the mikvah
            if mikvah_calendar:
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

                # get the saved appointments for this date
                mikvah_appointments = Appointment.objects.filter(mikvah_id=mikvah_id, date=date)
                print('appointments', mikvah_appointments)
                slots = Slots.objects.filter(mikvah_calendar=mikvah_calendar)

                # Excluding the slots that already have saved appointment to prevent double appointment for the same time
                for appointment in mikvah_appointments:
                    slots = slots.exclude(start_time__gte=appointment.start, end_time__lte=appointment.end)

            else:
                return HttpResponse('This Mikvah has no Calendar updated')

        else:
            return HttpResponse('form is not valid')

    context = {'form': form, 'slots': slots, 'mikvah_id': mikvah_id.mikvah_id}
    return render(request, 'website/new_appointment.html', context)


def save_appointment_view(request, mikvah_id):
    # View to save new appointments in the client account mikvah account
    mikvah_id = Mikvah.objects.get(mikvah_id=mikvah_id)
    user = request.user
    if request.method == 'POST':
        # Get the selectioned slots and restricting them to choice of a maximum of 3
        selected_slots = request.POST.getlist('slot')
        if 1 <= len(selected_slots) <= 3:
            slots = Slots.objects.filter(pk__in=selected_slots)

            # Calculate start and end time of the appointment
            start_time = slots[0].start_time
            end_time = slots[len(slots) - 1].end_time

            # Get the date of the appointment from the form, translate to time format and extract the day of the week
            # to get to the calendar of the mikvah
            selected_date_str = request.POST.get('selected_date')
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            selected_date_weekly = selected_date.strftime('%A')

            # save appointment to be later used by the client and the pro behind the mikvah
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


def my_appointments_view(request):
    # View to display all the future appointments of the user
    appointments = Appointment.objects.filter(user=request.user, date__gte=timezone.now().date()).order_by('-date')
    context = {
        'appointments': appointments,
    }
    return render(request, 'website/my_appointments.html', context)


def my_past_appointments_view(request):
    # View to display all the past appointments of the user
    appointments = Appointment.objects.filter(user=request.user, date__lt=timezone.now().date())
    context = {
        'appointments': appointments,
    }
    return render(request, 'website/my_past_appointments.html', context)


def cancel_appointment_view(request):
    # Function to cancel an appointment by changing the 'Canceled' field from False to True.
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        appointment.canceled = True
        appointment.save()
        return redirect('website:my_appointments')
    else:
        return render(request, 'website/my_appointments.html')