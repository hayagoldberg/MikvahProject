from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from website.forms import MikvahForm
from website.models import Mikvah, MikvahCalendar, CHOICES_DAY, Appointment


def my_mikvah(request):
    if request.method == 'POST':
        if 'mikvah-calendar' in request.POST:
            return redirect('website:mikvah_calendar')
    else:
        user = request.user
        my_mikvahs = Mikvah.objects.filter(user=user)
        mikvah_ids = my_mikvahs.values_list('mikvah_id', flat=True)
        my_mikvah_calendars = MikvahCalendar.objects.all()
    context = {'mikvahs': my_mikvahs,
               'mikvah_calendars': my_mikvah_calendars, }
    return render(request, 'website/my_mikvah.html', context)


def add_mikvah(request):
    if request.method == "POST":
        form = MikvahForm(request.POST)
        if form.is_valid():
            mikvah = form.save(commit=False)
            mikvah.user = request.user
            mikvah.save()
            return redirect('website:my_mikvah')
    else:
        form = MikvahForm()
    context = {
        'form': form,
    }
    return render(request, 'website/add_mikvah.html', context)


def user_group_is_professional(user):
    return user.groups.filter(name='Professional').exists()


@user_passes_test(user_group_is_professional)
def pro_page_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'my-mikvah' in request.POST:
                return redirect('website:my_mikvah')
            elif 'add-mikvah' in request.POST:
                return redirect('website:add_mikvah')
        return render(request, 'website/pro_page.html')
    else:
        return redirect('website:index')


@user_passes_test(user_group_is_professional)
def mikvah_calendar_view(request, mikvah_id):
    days_of_week = CHOICES_DAY
    if request.method == "POST":
        mikvah = Mikvah.objects.get(mikvah_id=mikvah_id)
        for i in range(1, 8):
            day = request.POST.get(f"day_{i}")
            opening_time = request.POST.get(f"opening_time_{i}")
            closing_time = request.POST.get(f"closing_time_{i}")
            mikvah_calendar = MikvahCalendar(
                day=day,
                opening_time=opening_time,
                closing_time=closing_time,
                mikvah_id=mikvah,
            )
            mikvah_calendar.save()
            return redirect('website:my_mikvah')

    context = {
        'days_of_week': days_of_week,
        }
    return render(request, 'website/mikvah_calendar.html', context)


def mikvah_appointments_view(request, mikvah_id):
    mikvah = Mikvah.objects.get(mikvah_id=mikvah_id)
    appointments = Appointment.objects.filter(mikvah_id=mikvah)
    context = {
       'appointments': appointments,
       'mikvah_id': mikvah_id
    }
    return render(request, 'website/mikvah_appointments.html', context)

