import os
import django
import random
from faker import Faker
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
django.setup()

from main.models import Student, Course, Grade

def main():
    fake = Faker('ru_RU')

    # Очистка существующих данных
    Course.objects.all().delete()
    Student.objects.all().delete()
    Grade.objects.all().delete()

    # Создание курсов
    courses = []
    for code, label in Course.academic_sub:  
        for i in range(1, 4): 

            start_date = fake.date_between(start_date='-180d', end_date='-28d')

            end_date = fake.date_between(start_date=start_date, end_date=start_date + timedelta(days=90))
            
            week_days_codes = [day[0] for day in Course.week_days]
            num_days = random.randint(1, 3)
            days_of_week = random.sample(week_days_codes, num_days)

            course, _ = Course.objects.get_or_create(
                name=code,
                course_num=i,
                defaults={
                    'start_date': start_date,
                    'end_date': end_date,
                    'description': f'{label} — поток {i}',
                    'days_of_week': days_of_week,
                }
            )
            courses.append(course)

    # Создание студентов
    students = []
    for _ in range(50):
        first = fake.first_name()
        last = fake.last_name()
        student, _ = Student.objects.get_or_create(
            name=first,
            surname=last,
            defaults={
                'age': random.randint(18, 60),
                'sex': random.choice(['m', 'f']),
                'active': random.choice([True, False]),
            }
        )
        # Случайные курсы для студента (от 1 до 4)
        student.course.set(random.sample(courses, random.randint(1, min(4, len(courses)))))
        students.append(student)

    # Создание оценок
    grades = []
    for st in students:
        st_courses = list(st.course.all())
        for _ in range(20):  # по n оценок на студента
            course = random.choice(st_courses)
            grade_val = random.randint(0, 10)  # оценка от 0 до 10
            date = fake.date_between(start_date='-90d', end_date='today')
            homework = fake.sentence(nb_words=10)  # случайное ДЗ
            grades.append(Grade(
                person=st,
                course=course,
                grade=grade_val,
                date=date,
                homework=homework
            ))

    if grades:
        Grade.objects.bulk_create(grades, batch_size=1000)

    print('Seed complete:',
          'courses =', Course.objects.count(),
          'students =', Student.objects.count(),
          'grades =', Grade.objects.count())

if __name__ == '__main__':
    main()