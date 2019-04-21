from django.urls import path
from . import views as timetable_views

urlpatterns = [
    path('', timetable_views.CalendarView.as_view(), name='timetable'),
]