from django import forms
from home.models import Course, Instructor, Agenda, Task
from timetable.models import Class
from django.forms.widgets import TextInput
from tempus_dominus.widgets import TimePicker, DatePicker, DateTimePicker
from .widgets import ColorPickerWidget

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'section', 'instructor','color',)
        widgets = {
            'color': ColorPickerWidget(),
        }

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'user'):
            self.user = kwargs.pop('user')
        
        super(CourseForm, self).__init__(*args, **kwargs) 
        self.fields['instructor'].queryset = Instructor.objects.filter(user=self.user) 

    def save(self, commit=True):
        course = super(CourseForm, self).save(commit=False)
        course.user = self.user
        
        if commit:
            course.save()
        
        return course 


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ('name', 'email', 'room_no', 'start_time', 'end_time', )
        
        widgets = {
            'start_time': TimePicker(
                options= {
                    'useCurrent' : True,
                    'format': 'hh:mm A',         # Format settings: https://momentjs.com/docs/#/displaying/format/
                },

                attrs={
                   'append': 'far fa-clock',
                },
            ),
            'end_time': TimePicker(
                options= {
                    'useCurrent' : True,
                    'format': 'hh:mm A',         # Format settings: https://momentjs.com/docs/#/displaying/format/
                },

                attrs={
                    'append': 'far fa-clock',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'user'):
            self.user = kwargs.pop('user')
        super(InstructorForm, self).__init__(*args, **kwargs)  
        


    def save(self, commit=True):
        instr = super(InstructorForm, self).save(commit=False)
        instr.user = self.user
        
        if commit:
            instr.save()
        
        return instr   


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('course', 'day', 'start_time','end_time', 'room',)
        widgets = {
            'start_time': TimePicker(
                options= {
                    'useCurrent' : True,
                    'format': 'hh:mm A',         # Format settings: https://momentjs.com/docs/#/displaying/format/
                },

                attrs={
                   'append': 'far fa-clock',
                },
            ),
            'end_time': TimePicker(
                options= {
                    'useCurrent' : True,
                    'format': 'hh:mm A',         # Format settings: https://momentjs.com/docs/#/displaying/format/
                },

                attrs={
                    'append': 'far fa-clock',
                },
            ),
        }
        

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'user'):
            self.user = kwargs.pop('user')
        
        super(ClassForm, self).__init__(*args, **kwargs)  
        self.fields['course'].queryset = Course.objects.filter(user=self.user) 

    def save(self, commit=True):
        instr = super(ClassForm, self).save(commit=False)
        instr.user = self.user
        
        if commit:
            instr.save()
        
        return instr     


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ('course', 'start_time', 'topic','agenda_type',)

        widgets = {
            'start_time': DatePicker(
                # options={
                #     'minDate': '2009-01-20',
                #     'maxDate': '2017-01-20',
                # },
            ),
        }

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'user'):
            self.user = kwargs.pop('user')
        
        super(AgendaForm, self).__init__(*args, **kwargs) 
        self.fields['course'].queryset = Course.objects.filter(user=self.user)
        
    def save(self, commit=True):
        agenda = super(AgendaForm, self).save(commit=False)
        agenda.user = self.user
        
        if commit:
            agenda.save()
        
        return agenda 
    


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('date', 'desc',)

        widgets = {
            'date': DatePicker(
                # options={
                #  W   'minDate': '2009-01-20',
                #     'maxDate': '2017-01-20',
                # },
            ),
        }

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'user'):
            self.user = kwargs.pop('user')
        
        super(TaskForm, self).__init__(*args, **kwargs) 

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        task.user = self.user
        
        if commit:
            task.save()
        
        return task 