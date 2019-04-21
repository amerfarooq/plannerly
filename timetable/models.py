from django.db import models
from home.models import Course
from users.models import User
from datetime import datetime

WEEK_DAYS = (
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
)

class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=WEEK_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=10)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'{self.course}' +  ' starts at ' + f'{self.start_time}' + ' in Room' + f'{self.room}'
