from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('client-page/', views.client_page_view, name='client_page'),
    path('pro-page/', views.pro_page_view, name='pro_page'),
    path('pro-page/my-mikvah/', views.my_mikvah, name='my_mikvah'),
    path('pro-page/add-mikvah/', views.add_mikvah, name='add_mikvah'),
    path('result-page/', views.search_result_view, name='search_result'),
    path('mikvah-calendar/<int:mikvah_id>', views.mikvah_calendar_view, name='mikvah_calendar'),
    path('mikvah-appointments/<int:mikvah_id>/', views.mikvah_appointments_view, name='mikvah_appointments'),
    path('new-appointment/<int:mikvah_id>', views.new_appointment_view, name='new_appointment'),
    path('save-appointment/<int:mikvah_id>', views.save_appointment_view, name='save_appointment'),
    path('my-appointments/', views.my_appointments_view, name='my_appointments'),
    path('my-past-appointments/', views.my_past_appointments_view, name='my_past_appointments'),
    path('cancel-appointment/', views.cancel_appointment_view, name='cancel_appointment'),

]
