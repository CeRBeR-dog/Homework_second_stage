from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView

from .forms import *
from .models import Student, Course, Grade, Profile
from .decorators import teacher_required
from collections import defaultdict
from datetime import timedelta


# Create your views here.

def index(request):
    return render(request, 'main/index.html')

@login_required(login_url='/login/')
def students(request):
    students = Student.objects.all()
    paginator_student = Paginator(students, 15)

    page_number = request.GET.get('page')
    page_obj = paginator_student.get_page(page_number)

    return render(request, 'main/students.html', 
                    context={'students': students,
                             'page_obj': page_obj})


@login_required(login_url='/login/')
def student_detail(request, student_id):
    student = get_object_or_404(Student, id = student_id)
    grades_list = Grade.objects.filter(person = student)
    paginator_grades = Paginator(grades_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator_grades.get_page(page_number)

    custom_page_range = page_obj.paginator.get_elided_page_range(
        page_obj.number,
        on_each_side = 1,
        on_ends = 1
    )

    return render(request, 'main/student_detail.html', 
                  context= {'student': student,
                            'page_obj': page_obj,
                            'custom_page_range': custom_page_range}
                  )


@login_required(login_url='/login/')
@teacher_required
def student_add(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('students')
    
    else:
        form = StudentAddForm()
    return render(request, 'main/student_form.html',
                  {'form': form})


@login_required(login_url='/login/')
def courses(request):
    course = Course.objects.all()
    paginator_course = Paginator(course, 5)

    page_number = request.GET.get('page')
    page_obj = paginator_course.get_page(page_number)

    return render(request, 'main/courses.html',
                  context = {'courses': course,
                             'page_obj': page_obj},
                )


@login_required(login_url='/login/')
@teacher_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id = course_id)
    # student = get_object_or_404(Student, id = student_id)
    
    sort_param = request.GET.get('sort', '-date')

    allowed_sorts = ['grade', '-grade', 'date', '-date', 'person__surname', '-person__surname']
    if sort_param not in allowed_sorts:
        sort_param = '-date'
   
    grades_list = Grade.objects.filter(
        course=course).select_related('person').order_by(sort_param)
    
    paginator_grades = Paginator(grades_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator_grades.get_page(page_number)

    custom_page_range = page_obj.paginator.get_elided_page_range(
        page_obj.number,
        on_each_side = 1,
        on_ends = 1
    )
    
    return render(request, 'main/course_detail.html', 
                  {'course': course,
                   'page_obj': page_obj,
                    'custom_page_range': custom_page_range,
                    'current_sort': sort_param}
                  )


@login_required(login_url='/login/')
@teacher_required
def grades_journal(request):
    students = Student.objects.prefetch_related('grades')
    return render(request,
                    'main/grades_journal.html',
                    {'students': students}
                    )


# вспомогательная функция 
def get_leeson_dates(course):
    if not course.start_date or not course.end_date:
        return[]
    
    day_code = {
        'mon': 0,
        'tue': 1,
        'wed': 2,
        'thu': 3,
        'fri': 4,
        'sat': 5,
    }

    selected_day = [day_code[day] for day in course.days_of_week if day in day_code]
    if not selected_day:
        return[]
    
    dates = []
    current = course.start_date
    delta = timedelta(days=1)
    while current <= course.end_date:
        if current.weekday() in selected_day:
            dates.append(current)
        current += delta
    return dates


@login_required(login_url='/login/')
@teacher_required
def course_journal(request, course_id):
    course = get_object_or_404(Course, id = course_id)

    students = course.students.all()
    grades = Grade.objects.filter(course=course).select_related('person')

    dates =  get_leeson_dates(course)
    if not dates:
        dates = sorted(set(grade.date for grade in grades if grade.date))

    journal = defaultdict(dict)
    homework_on_date = {}

    for grade in grades:
        if grade.date:
            journal[grade.person.id][grade.date] = grade.grade
            if grade.date not in homework_on_date and grade.homework:
                homework_on_date[grade.date] = grade.homework

    context = {
        'course': course,
        'students': students,
        'dates': dates,
        'journal': journal,
        'homework_on_date': homework_on_date
    }

    return render(request, 'main/course_journal.html', context)


@login_required(login_url='/login/')
@teacher_required
def update_grade(request):
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        date_str = request.POST.get('date')
        gradue_value = request.POST.get('grade_value')

        if not all([student_id, course_id, date_str, gradue_value]):
            return redirect(request.META.get('HTTP_REFERER', 'journal'))
        
        if gradue_value == 'delete':
            Grade.objects.filter(
                person_id = student_id, 
                course_id = course_id, 
                date = date_str
            ).delete()
            
        else:
            val = 0 if gradue_value == 'н' else int(gradue_value)

            Grade.objects.update_or_create(
                person_id = student_id,
                course_id = course_id,
                date = date_str,
                defaults={'grade': val}
            )  
        
        return redirect(request.META.get('HTTP_REFERER', 'journal'))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    # success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
    
    
class LoginUser(LoginView):
    template_name = 'main/login.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('index')

class LogoutUser(LogoutView):
    next_page = reverse_lazy('index')