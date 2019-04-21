from django.contrib import admin
from .models import Course, Instructor, Agenda, Task
from .forms import CourseForm

admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Agenda)
admin.site.register(Task)

class ColorAdmin(admin.ModelAdmin):
    form = CourseForm
    filter_horizontal = ('questions',)
    fieldsets = (
        (None, {
            'fields': (('name', 'letter'), 'questions', 'color')
            }),
        )