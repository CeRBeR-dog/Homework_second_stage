from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def students(request):
    students = Student.objects.all()
    return render(request, 'main/students.html', 
                    context={'students':students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id = student_id)
    return render(request, 'main/student_detail.html', {'student': student})

def courses(request):
    course = Course.objects.all()
    return render(request, 'main/courses.html',
                   {'courses': course},
                )

def course_detail(request, course_id):
    course = get_object_or_404(Course, id = course_id)
    return render(request, 'main/course_detail.html', {'course': course})

def grades_journal(request):
    students = Student.objects.prefetch_related('grades')
    return render(request, 'main/grades_journal.html', {'students': students})