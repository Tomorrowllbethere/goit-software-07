from models import Student, Teacher, Group, Subject, Points_table
from sqlalchemy import create_engine, func, desc, subquery
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:mysecret@localhost:5432/user"
engine = create_engine(DATABASE_URL)
# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    result = session.query(Student.name, func.round(func.avg(Points_table.points), 2).label('avg_grade'))\
    .select_from(Points_table).join(Student, Student.id== Points_table.student_info).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result

def select_2():
    query = (
    session.query(
        Student.id.label('students_id'),
        Student.name.label('students_name'),
        Student.group_id.label('students_group_id'),
        func.round(func.avg(Points_table.points), 2).label('average_points')
    )
    .join(Points_table, Points_table.student_info == Student.id)
    .join(Subject, Subject.subject_name == 'Astronomy')
    .filter(Points_table.lesson_id == Subject.id)
    .group_by(Student.id)
    .order_by(func.avg(Points_table.points).desc())
    .limit(1)
)
    return query

def select_3():
    query = (
        session.query(
            Group.group_name.label('group_name'),
            func.avg(Points_table.points).label('average_points')
        )
        .select_from(Group)
        .join(Student)
        .join(Points_table, Points_table.student_info == Student.id)
        .join(Subject, Subject.subject_name == 'Astronomy')
        .filter(Points_table.lesson_id == Subject.id)
        .group_by(Group.group_name)
    )
    return query

def select_4():
    subquery = (
    session.query(
        func.avg(Points_table.points).label('average_points')
    )
    .select_from(Points_table)
    .join(Student, Points_table.student_info == Student.id)
    .group_by(Student.id)
    .subquery()
    )
    query = (
        session.query(
            func.avg(subquery.c.average_points).label('overall_average_points')
        )
    )
    return query

def select_5():
    query = (
    session.query(
        Subject.teachers_id.label('teacher_id'),
        Teacher.fullname.label('teacher_name'),
        Subject.subject_name.label('subject_name')
    ).select_from(Subject)
    .join(Teacher, Teacher.id == Subject.teachers_id)
    .order_by(Subject.teachers_id)
)
    return query

def select_6():
    group = (session.query(
        Student.name.label('student_name'),
        Group.group_name.label('group_name')
    )
    .join(Group, Student.group_id == Group.id)  # Об'єднання за зовнішнім ключем
    .filter(Group.group_name == 'Lit-1')  # Фільтрація за ім'ям групи
    .order_by(Student.name)  # Сортування за ім'ям студента
)
    result = group.all()
    return result

def select_7():
    query = (session.query(
            Student.name.label('student_name'),
            Points_table.points.label('student_points')
        )
        .join(Points_table, Student.id == Points_table.student_info ) # Об'єднання з оцінками студентів
        .join(Group, Student.group_id == Group.id)  # Об'єднання з групами
        .join(Subject, Points_table.lesson_id == Subject.id)  # Об'єднання з предметами
        .filter(Group.group_name == 'Lit-1')  # Фільтрація за ідентифікатором групи
        .filter(Subject.subject_name == 'Astronomy')  # Фільтрація за назвою предмета
    )
# Виконання запиту та отримання результатів
    results = query.all()
    return results

def select_8():
    query = (session.query(
                Subject.subject_name.label('subject_name'),
                func.avg(Points_table.points).label('average_points')
            )
            .select_from(Points_table)
            .join(Subject, Points_table.lesson_id == Subject.id)  # Об'єднання з предметами
            .join(Teacher, Subject.teachers_id == Teacher.id)  # Об'єднання з викладачем
            .filter(Teacher.fullname == 'Jerry Kelley')  # Фільтрація за ім'ям викладача
            .group_by(Subject.subject_name)  # Групування за ім'ям предмету
        )
    # Виконання запиту та отримання результатів
    results = query.all()
    return results

def select_9(student_name):
    query = (session.query(
                Subject.subject_name.label('course_name')
            )
            .select_from(Subject)
            .join(Points_table, Points_table.lesson_id == Subject.id)  # Об'єднання з оцінками
            .join(Student, Student.id == Points_table.student_info)  # Об'єднання зі студентами
            .filter(Student.name == student_name)  # Фільтрація за ім'ям студента
            .group_by(Subject.subject_name)  # Групування за ім'ям курсу
            .order_by(Subject.subject_name)  # Сортування за ім'ям курсу
            .all()
        )
    return query 

def select_10(teacher_name, student_name):
    query = (session.query(
                Subject.subject_name.label('course_name')
            )
            .select_from(Subject)
            .join(Points_table, Points_table.lesson_id == Subject.id)  # Об'єднання з оцінками
            .join(Teacher, Teacher.id == Subject.teachers_id)  # Об'єднання з викладачами
            .join(Student, Student.id == Points_table.student_info)  # Об'єднання зі студентами
            .filter(Teacher.fullname == teacher_name)  # Фільтрація за ім'ям викладача
            .filter(Student.name == student_name)  # Фільтрація за ім'ям студента
            .group_by(Subject.subject_name)  # Групування за ім'ям курсу
            .order_by(Subject.subject_name)  # Сортування за ім'ям курсу
            .all()
        )
    return query

if __name__ == '__main__':
    ''''''
    query = select_1()
    for result in query:
        print(result)
    ''''''
    query = select_2()
    for result in query:
        print(result)
    ''''''
    query = select_3()
    for result in query:
        print(result)
    ''''''   
    query = select_4()
    for result in query:
        print(result)    
    ''''''
    query = select_5()
    for result in query:
        print(result)    
    '''''' 
    query = select_6()
    for result in query:
        print(result)
    ''''''
    query = select_7()
    for result in query:
        print(result)    
    '''''' 
    query = select_8()
    for result in query:
        print(result)
    ''''''
    query = select_9(student_name='Vanessa Gardner')
    for result in query:
        print(result)    
    '''''' 
    query = select_10(teacher_name= 'Jamie Ramirez', student_name='Erica Burke')
    for result in query:
        print(result)
    ''''''