from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='home'),
    path('agenda_calendar/',views.CalendarView.as_view(), name='calendar'),
    path('agenda_list_daily/',views.agenda_list_daily, name='agenda_list_daily'),
    path('agenda_list_monthly/',views.agenda_list_monthly, name='agenda_list_monthly'),
    path('agenda_list_yearly/',views.agenda_list_yearly, name='agenda_list_yearly'),
    path('courses/', views.courses, name='courses'),
    path('timetable/', views.timetable, name='timetable'),
    path('instructors/', views.instructors, name='instructors'),
    path('agenda_list/delete_agenda_item/', views.delete_agenda_item),
    path('courses/delete_course/', views.delete_course),
    path('instructors/delete_instr/', views.delete_instr),
    path('timetable/delete_class/', views.delete_class),
    path('delete_task/',views.delete_task),
    path('timetable/get_class/', views.get_class),
    # path('nextcalendar', views.CalendarView.as_view, name='calendar'),
    # url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'), # here
    url(r'^agenda/new/$', views.agenda, name='agenda_new'),
    # url(r'^agenda/edit/(?P<event_id>\d+)/$', views.agenda, name='agenda_edit'),
]