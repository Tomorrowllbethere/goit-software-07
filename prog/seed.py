from connect import session
from models import Student, Teacher, Group, Subject, Points_table
import faker
import datetime 
from random import randint, choice
lesson_names = './lessons.txt'
group_names = './students_group.txt'
NUMBER_STUDENTS = 30
NUMBER_TEACHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GROUPS = 3
NUMBER_POINTS = 20
fake_data = faker.Faker()

def generate_persons():# -> tuple[list, list]:
    fake_students = []
    fake_teachers = []
    for _ in range(NUMBER_STUDENTS):
        fake_students.append(fake_data.name())
    for _ in range(NUMBER_TEACHERS):
        fake_teachers.append(fake_data.name())

    return fake_students, fake_teachers

def random_groups():# -> list:
    foldered_groups = []
    with open(group_names, 'r') as f:
        groups = f.readlines()
        for group in groups:
            foldered_groups.append(group.strip() )
    fake_groups = []
    for _ in range(NUMBER_GROUPS):
        some_group = choice(foldered_groups)
        fake_groups.append(some_group)
    return fake_groups

def making_subject():# -> list:
    all_lessons =[]
    lessons=[]
    with open(lesson_names, "r+") as f:
        lessons_file = f.readlines()
        for les in lessons_file:
            all_lessons.append(les.strip())
    for _ in range(NUMBER_SUBJECTS):
        l = choice(all_lessons)
        lessons.append(l)
    return lessons

def preparing_date():
    fake_points = []
    fake_datestamp = []
    for i in range(30):
        period =  datetime.datetime.today()- datetime.timedelta(days=i, minutes=float(randint(1,59)), hours=float(randint(1,12)))
        date = datetime.datetime.strftime(period, '%Y-%m-%d')
        fake_datestamp.append(date)
    for _ in range(50):
        fake_points.append(float(randint(45, 100)))
    return fake_datestamp, fake_points

def filling(student, datestamp, lessons, fake_groups, points):
    try:
        g = choice(fake_groups) #вибираємо групу
        group = session.query(Group).filter_by(group_name = g).first() #робимо запит, чи вже існує група
        if group:#якщо група вже існує
            new = Student(name = student, group_id = group.id)#створюємо студента
            session.add(new)
            session.commit()
            for _ in range(NUMBER_POINTS):
                l= choice(lessons)# вибираємо урок
                less = session.query(Subject).filter_by(subject_name = l).first()# робимо запит, чи існує такий урок
                if less:# якщо існує, використовуємо отриману інформацію
                    new_info = Points_table(points = choice(points), date_of = choice(datestamp), student_info = new.id, lesson_id = less.id)
                    session.add(new_info)
                    session.commit()
                else:# якщо не існує, створюємо такий обєкт
                    new_subject = Subject(subject_name = l, teachers_id = randint(1, NUMBER_TEACHERS), group_id = group.id)
                    session.add(new_subject)
                    session.commit()
                    new_info = Points_table(points = choice(points), date_of = choice(datestamp), student_info = new.id, lesson_id = new_subject.id)
                    session.add(new_info)
            return session.commit()
        else: #якщо не існує група
            new_group = Group(group_name = g) # створюємо групу
            session.add(new_group)
            session.commit()
            new = Student(name = student, group_id = new_group.id)#створюємо студента
            session.add(new)
            session.commit()
            for _ in range(NUMBER_POINTS):
                l= choice(lessons)# вибираємо урок
                less = session.query(Subject).filter_by(subject_name = l).first()# робимо запит, чи існує такий урок
                if less:# якщо існує, використовуємо отриману інформацію
                    new_info = Points_table(points = choice(points), date_of = choice(datestamp), student_info = new.id, lesson_id = less.id)
                    session.add(new_info)
                    session.commit()
                else:# якщо не існує, створюємо такий обєкт
                    new_subject = Subject(subject_name = l, teachers_id = randint(1, NUMBER_TEACHERS), group_id = new_group.id)
                    session.add(new_subject)
                    session.commit()
                    new_info = Points_table(points = choice(points), date_of = choice(datestamp), student_info = new.id, lesson_id = new_subject.id)
                    session.add(new_info)
            return session.commit()
    except Exception as e:
            print(f'ERROR: {e}')

if __name__ == '__main__':
    students, teachers = generate_persons()
    fake_groups = random_groups()
    lessons = making_subject()
    datestamp, points = preparing_date()
    '''adding teachers'''
    for teacher in teachers:
        new = Teacher(fullname = teacher)
        session.add(new)
    
    session.commit()
    
    '''adding students'''
    '''для кожного студента'''
    for student in students:
        filling(student, datestamp, lessons, fake_groups, points)
        

    session.commit()
    '''
    1

    alembic revision --autogenerate -m "Опис змін"

    2

    alembic upgrade head

    '''

