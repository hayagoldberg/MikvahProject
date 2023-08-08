from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('client_page/', views.client_page_view, name='client_page'),
    path('pro_page/', views.pro_page_view, name='pro_page'),
    path('pro_page/my_mikvah/', views.my_mikvah, name='my_mikvah'),
    path('pro_page/add_mikvah/', views.add_mikvah, name='add_mikvah'),
    path('result_page/', views.search_result_view, name='search_result'),
    path('mikvah_calendar/<int:mikvah_id>', views.mikvah_calendar_view, name='mikvah_calendar'),
    path('mikvah_appointments/<int:mikvah_id>/', views.mikvah_appointments_view, name='mikvah_appointments'),
    path('new_appointment/<int:mikvah_id>', views.new_appointment_view, name='new_appointment'),
    path('save_appointment/<int:mikvah_id>', views.save_appointment_view, name='save_appointment'),
    path('my_appointments/', views.my_appointments_view, name='my_appointments'),
    path('my_past_appointments/', views.my_past_appointments_view, name='my_past_appointments'),
    path('cancel_appointment/', views.cancel_appointment_view, name='cancel_appointment'),

]
