from django.shortcuts import render, get_object_or_404
from .models import Student, Course, Grade, Profile
from collections import defaultdict

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
    course = get_object_or_404(Course, id = course_id)
    return render(request, 
                  'main/course_detail.html', 
                  {'course': course}
                  )

def grades_journal(request):
    students = Student.objects.prefetch_related('grades')
    return render(request,
                    'main/grades_journal.html',
                    {'students': students}
                    )

def course_journal(request, course_id):
    course = get_object_or_404(Course, id = course_id)

    students = course.students.all()
    grades = Grade.objects.filter(course=course).select_related('person')

    dates = sorted(set(grade.date for grade in grades))

    journal = defaultdict(dict)

    for grade in grades:
        journal[grade.person.id][grade.date] = grade.grade

    context = {
        'course': course,
        'students': students,
        'dates': dates,
        'journal': journal,
    }

    return render(request, 'main/course_journal.html', context)