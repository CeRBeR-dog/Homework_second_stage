from django.shortcuts import render, get_object_or_404
from .models import Student, Course, Grade, Profile
from collections import defaultdict
from datetime import timedelta

# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def students(request):
    students = Student.objects.all()
    return render(request, 'main/students.html', 
                    context={'students':students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id = student_id)
    return render(request, 'main/student_detail.html', 
                  {'student': student}
                  )

def courses(request):
    course = Course.objects.all()
    return render(request, 'main/courses.html',
                   {'courses': course},
                )

def course_detail(request, course_id):
    courses = get_object_or_404(Course, id = course_id)
    return render(request, 
                  'main/course_detail.html', 
                  {'course': courses}
                  )

def grades_journal(request):
    students = Student.objects.prefetch_related('grades')
    return render(request,
                    'main/grades_journal.html',
                    {'students': students}
                    )

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