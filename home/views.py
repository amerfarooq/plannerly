from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from home.forms import CourseForm, InstructorForm, ClassForm , AgendaForm, TaskForm
from django.contrib import messages
from home.models import Agenda, Course, Task, Instructor
from timetable.models import Class
from .models import *
from django.views.decorators.csrf import csrf_exempt
import operator
from .utils import Calendar
from django.shortcuts import get_object_or_404
from crispy_forms.utils import render_crispy_form

#some libraries for calendar...
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar

@login_required(login_url='login')
def home(request):
    agenda_items = Agenda.objects.filter(user = request.user).order_by('-start_time')
    agenda_items = agenda_items[::-1]
    # print(agenda_items[0].start_time)


    todays_items = []
    obj = datetime.now()
    for item in agenda_items:
        if item.start_time.day == obj.day:
            todays_items.append(item)


    tasks = Task.objects.filter(user = request.user)

    classes = get_todays_classes(request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(None, user=request.user)
        

    return render(request, 'home/dashboard.html', {'form':form,'tasks':tasks, 'agenda_items':todays_items, 'classes':classes})

@login_required(login_url='login')
def agenda_list_daily(request):
    agenda_items = Agenda.objects.filter(user = request.user).order_by('-start_time')
    agenda_items = agenda_items[::-1]
    # print(agenda_items[0].start_time)


    todays_items = []
    obj = datetime.now()
    for item in agenda_items:
        if item.start_time.day == obj.day:
            todays_items.append(item)

    if request.method == 'POST':
        form = AgendaForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('agenda_list_daily')

    else:
        form = AgendaForm(None, user=request.user)
        
    return render(request, 'home/agenda_list_daily.html', {'form':form, 'agenda_items':todays_items})


@login_required(login_url='login')
def agenda_list_monthly(request):
    agenda_items = Agenda.objects.filter(user = request.user).order_by('-start_time')
    agenda_items = agenda_items[::-1]
    # print(agenda_items[0].start_time)


    todays_items = []
    obj = datetime.now()
    for item in agenda_items:
        if item.start_time.month == obj.month:
            todays_items.append(item)

    if request.method == 'POST':
        form = AgendaForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('agenda_list_monthly')

    else:
        form = AgendaForm(None, user=request.user)
        
    return render(request, 'home/agenda_list_monthly.html', {'form':form, 'agenda_items':todays_items})

@login_required(login_url='login')
def agenda_list_yearly(request):
    agenda_items = Agenda.objects.filter(user = request.user).order_by('-start_time')
    agenda_items = agenda_items[::-1]
    # print(agenda_items[0].start_time)


    todays_items = []
    obj = datetime.now()
    for item in agenda_items:
        if item.start_time.year == obj.year:
            todays_items.append(item)

    if request.method == 'POST':
        form = AgendaForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('agenda_list_yearly')

    else:
        form = AgendaForm(None, user=request.user)
        
    return render(request, 'home/agenda_list_yearly.html', {'form':form, 'agenda_items':todays_items})


@login_required(login_url='login')
def courses(request):
    Courses = Course.objects.filter(user = request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, user=request.user)
    
        if form.is_valid():
            form.save()
            return redirect('courses')
        
        else:
            print (form.cleaned_data)

    else:
        form = CourseForm(None, user=request.user)
        
    return render(request, 'home/courses.html', {'form':form, 'courses':Courses})


@login_required(login_url='login')
def instructors(request):
    instructors = Instructor.objects.filter(user=request.user)

    if request.method == 'POST':
        form = InstructorForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('instructors')

    else:
        form = InstructorForm(None, user=request.user)
        
    return render(request, 'home/instructors.html', {'form':form, 'Instructors':instructors})



@login_required(login_url='login')
def timetable(request):

    if request.method == 'POST':
        form = ClassForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('timetable')

    else:
        form = ClassForm(None, user=request.user)
        
        mon_classes = sorted((Class.objects.filter(user=request.user, day="mon")), key=operator.attrgetter('start_time'))
        tue_classes = sorted((Class.objects.filter(user=request.user, day="tue")), key=operator.attrgetter('start_time'))
        wed_classes = sorted((Class.objects.filter(user=request.user, day="wed")), key=operator.attrgetter('start_time'))
        thu_classes = sorted((Class.objects.filter(user=request.user, day="thu")), key=operator.attrgetter('start_time'))
        fri_classes = sorted((Class.objects.filter(user=request.user, day="fri")), key=operator.attrgetter('start_time'))
    
    return render(request, 'home/timetable.html', {'form':form, 'mon':mon_classes, 'tue':tue_classes,
                                                                'wed':wed_classes, 'thu':thu_classes, 
                                                                'fri':fri_classes })


class CalendarView(generic.ListView):
    model = Agenda
    template_name = 'home/agenda.html'
# @login_required(login_url='login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(request=self.request, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def agenda(request):
    # instance = Agenda()
    # if event_id:
    #     instance = get_object_or_404(Agenda, pk=event_id)
    # else:
    #     instance = Agenda()
    print("in agenda view")
    if request.method == 'POST':
        form = AgendaForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('calendar')
    
    else:
        form = AgendaForm(None, user=request.user)
        
    return render(request, 'home/agendainput.html', {'form':form})


    # form = AgendaForm(request.POST or None, instance=instance, user=request.user)
    # form.save() 
    # return HttpResponseRedirect(reverse('calendar'))
    # return render(request, 'home/agenda.html', {'form': form})




@login_required(login_url='login')
@csrf_exempt
def delete_agenda_item(request):
    
    if (request.method == 'POST'):
        pk = request.POST['pk']
        Agenda.objects.filter(pk=pk).delete()

        HttpResponse('')


@login_required(login_url='login')
@csrf_exempt
def delete_task(request):
    
    if (request.method == 'POST'):
        pk = request.POST['pk']
        Task.objects.filter(pk=pk).delete()

        HttpResponse('')


@login_required(login_url='login')
@csrf_exempt
def delete_course(request):
    
    if (request.method == 'POST'):
        pk = request.POST['pk']
        Course.objects.filter(pk=pk).delete()

        HttpResponse('')


@login_required(login_url='login')
@csrf_exempt
def delete_instr(request):
    
    if (request.method == 'POST'):
        pk = request.POST['pk']
        Instructor.objects.filter(pk=pk).delete()

        HttpResponse('')


@login_required(login_url='login')
def index(request):
    return HttpResponse('hello')



@login_required(login_url='login')
@csrf_exempt
def delete_class(request):
    
    if (request.method == 'POST'):
        pk = request.POST['pk']
        Class.objects.filter(pk=pk).delete()

        HttpResponse('')


@login_required(login_url='login')
@csrf_exempt
def get_class(request):
    if request.method == "GET":
        pk = request.GET['pk']
        item = get_object_or_404(Class, pk=pk)
        form = ClassForm(instance=item, user=request.user)
        
        return HttpResponse(render_crispy_form(form)) 

@login_required(login_url='login')
@csrf_exempt
def agenda_new(request):
    if request.method == "GET":
        print("sdas")

        form = AgendaForm(user=request.user)
        
        return HttpResponse(render_crispy_form(form)) 


def get_todays_classes(user):
    weekday = datetime.today().weekday()
    day = None

    if weekday == 1:
        day = 'mon'
    elif weekday == 2:
        day = 'tue'
    elif weekday == 3:
        day = 'wed'
    elif weekday == 4:
        day = 'thu'
    elif weekday == 5:
        day = 'fri'
        
    return sorted((Class.objects.filter(user=user, day=day)), key=operator.attrgetter('start_time'))
    

