from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    
    name = models.CharField(max_length=30, 
                            verbose_name="Имя",
                            null=False,
                            blank=False,
                            # unique = True
                            #db_column #Имя столбца базы
                            # db_comment
                            # db_index 
                            # editable        
                            # error_messages # переопределить сообщения об ошибках - null, blank, invalid, unique_for_date        
                            # help_text #Дополнительный текст «помощи», который будет отображаться с виджетом формы.
                            # unique_for_date
                            )
    
    surname = models.CharField(max_length=30, 
                               verbose_name='Фамилия')
    
    age = models.SmallIntegerField(null=True, 
                                   blank=True, 
                                   verbose_name="Возраст", 
                                   validators=[MinValueValidator(18), 
                                               MaxValueValidator(99)])
    
    sex = models.CharField(
                        max_length=10,
                        choices=[('m', "Мужчина"),('f', "Женщина")],
                        verbose_name="Пол"
    )
    
    active = models.BooleanField(verbose_name='Активный', 
                                 null=True, blank=True)
    
    course = models.ManyToManyField(
                to='Course', 
                blank=True, 
                verbose_name="Посещаемые курсы", related_name="students")
    
                # course.student_set()
    
    # фото
    # курсы - связь
    
    def __str__(self):
        return f"{self.surname} {self.name}"
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты" 
        indexes = [models.Index(fields=['surname'])]
        unique_together = [['name', 'surname']]
        # db_table = 'students'
        ordering = ["surname"]



class Course(models.Model):
    academic_sub = [
        ('физ','Физика'),
        ('инф','Информатика'),
        ('хим','Химия'),
        ('мат','Математика'),
    ]

    week_days = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
    ]
    
    name = models.CharField(choices=academic_sub, 
                            max_length=20, 
                            verbose_name="Курс")

    course_num = models.SmallIntegerField(
                    default=1, 
                    verbose_name="Номер курса", 
                    validators=[MinValueValidator(1), MaxValueValidator(100)])
     
    start_date = models.DateField(verbose_name = 'Начало курса', null=True)

    end_date = models.DateField(verbose_name = 'Окончание курса', null=True)

    days_of_week = models.JSONField(default=list,
                                    blank=True,
                                    verbose_name="Дни недели")

    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        days = ', '.join([dict(self.week_days).get(d, d) for d in self.days_of_week])
        return f"{self.get_name_display()} - {self.course_num} ({days})"

    class Meta:
        unique_together = [['name', 'course_num']]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы" 
        ordering = ['name', 'course_num']
    

      
class Grade(models.Model):
    person = models.ForeignKey(
            Student, 
            on_delete=models.CASCADE,
            related_name="grades",
            verbose_name = 'Чья оценка')
    
    grade = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name = 'Оценка'
    )
    
    homework = models.TextField(
        blank = True,
        verbose_name='Домашнее задание'
    )

    course = models.ForeignKey(
            Course, 
            null=True,
            on_delete=models.CASCADE,
            verbose_name = 'Курс')
    
    date = models.DateField(verbose_name = 'Дата оценки', null=True)
    
    
    date_add = models.DateField(
            auto_now_add=True, 
            null=True,
            verbose_name = 'Дата добавления')
    
    date_update = models.DateField(
            auto_now=True,
            null=True,
            verbose_name = 'Дата изменения')

    

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

class Profile(models.Model):
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                related_name='profile',
                                verbose_name='Профиль')
    
    
    phone = models.CharField(max_length=20, 
                             blank=True,
                             verbose_name='Номер телефона')
    

    def __str__(self):
        return f'Профиль {self.user.username}'
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
