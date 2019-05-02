from django.db import models
from django.utils import timezone
from users.models import User
from datetime import date, datetime
from datetime import datetime
from django.urls import reverse

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    room_no = models.CharField(max_length=50)
    start_time = models.TimeField(verbose_name="office hours start")
    end_time = models.TimeField(verbose_name="office hours end")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    section = models.CharField(max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, blank=True, null=True, on_delete=models.SET_NULL,)
    color = models.CharField(max_length=7)

    def __str__(self):
        return f'{self.course_name}'
   

AGENDA_TYPES = (
    ('Quiz', 'Quiz'),
    ('Assignment', 'Assignment'),
)

class Agenda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateField()
    topic = models.TextField(max_length=50)
    agenda_type = models.CharField(max_length=15, choices=AGENDA_TYPES)

    def __str__(self):
        return f'{self.course}' + '-' + f'{self.start_time}'


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    desc = models.TextField(verbose_name="description",)

    def __str__(self):
        return f'{self.desc}' + '-' + f'{self.date}'