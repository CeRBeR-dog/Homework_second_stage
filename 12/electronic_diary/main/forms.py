from django import forms
from .models import Course, Student, Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CourseAddForm(forms.Form):
    
    sub = Course.academic_sub
    day = Course.days_of_week
    
    name = forms.ChoiceField(choices=sub, label="Название курса", required=True, 
                             help_text="Выберите название")
    
    course_num = forms.IntegerField(min_value=1, max_value=100, label="Номер курса")
    
    start_date = forms.DateField(widget=forms.DateInput(
                        attrs={'type':'date', 'class':'data123'}))
    end_date = forms.DateField(widget=forms.DateInput(
                        attrs={'type':'date', 'class':'data123'}))    

    days_of_week = forms.MultipleChoiceField(
        choices= day,
        widget= forms.CheckboxSelectMultiple,
        required= False,
        label= 'Дни занятий'
    )

    description = forms.CharField(widget=forms.Textarea(attrs={'rows':5}),
                                  required= False,
                                  label='Описание', 
                                  help_text='Краткое опимание курса')
    
    
# class CourseAddForm2(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = '__all__'      
#         # fields = ['name', 'start_date']  
        
#         widgets = {
#                 # 'start_date': forms.SelectDateWidget(), 
#                 'start_date': forms.DateInput(
#                                 attrs={'type':'date', 'class':'data123'}), 
#                 'end_date': forms.DateInput(
#                                 attrs={'type':'date', 'class':'data123'}),                 
#             }
        
        
class StudentAddForm(forms.ModelForm):   
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {'age': forms.NumberInput(attrs={'min': 18, 'max': 99}),}
        
        
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 18 or age > 99):
            raise ValidationError('Возраст должен быть от 18 до 99')
         
        
    # def save(self, commit: bool = ...) -> Any:        
    #     return super().save(commit)        
    
    
class RegisterUserForm(UserCreationForm):    
    
    firs_name = forms.CharField(max_length=30, 
                                required=True,
                                label='Имя', 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(max_length=30, 
                                required=True,
                                label='Фамилия', 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    
    class Meta:
        model =  User
        fields = ('username', 'first_name', 'last_name',
                 'password1', 'password2')
        
    def save(self, commit = True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user