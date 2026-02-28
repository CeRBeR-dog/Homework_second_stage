
from django.urls import path

from . import views

urlpatterns = [              
    path('', views.index, name='index'),

    path('students/', views.students, name='students'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),

    path('courses/', views.courses, name='courses'),  
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/journal/', views.course_journal, name='course_journal'), 
    
    path('grades/', views.grades_journal, name='grades_journal'),  
    
    
]