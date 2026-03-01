from django.contrib import admin
from django import forms
from .models import *

# admin.site.register(Student) 

# admin.site.register(Course)
admin.site.register(Grade)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'sex', 'short_name', 'average_grade', 'average_grade2')
    search_fields = ('name', 'surname')
    list_filter = ('sex', 'active')
    
    def average_grade(self, obj):
            # return '5'
        gs = [g.grade for g in obj.grades.all()]
        return round(sum(gs)/len(gs),2) if gs else '---'
    
    def average_grade2(self, obj):
        from django.db.models import Avg
        res = Grade.objects.filter(person=obj).aggregate(Avg('grade', default=0))
        return res['grade__avg']
    
    
    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."
    
    short_name.short_description = "Короткое имя"

class CourseAdminForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=Course.week_days,
        widget=forms.CheckboxSelectMultiple,
        label='Дни занятий',
        required=False
        
    )

    class Meta:
        model = Course
        fields = '__all__'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'phone')