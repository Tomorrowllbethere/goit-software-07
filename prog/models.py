'''Пам'ятати про використання for sqlalchemy 2.0.29'''
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base

# py project/models.py
Base = declarative_base()

# таблиця для зв'язку many-to-many між таблицями notes та tags
# stud_m2m_subj = Table(
#     "tud_m2m_subj",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("student", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
#     Column("subject", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
# )


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    group = relationship("Group", back_populates="students")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(250), nullable=False, unique=True)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(250), nullable=False)
    students = relationship("Student", back_populates="group")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(250), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    teachers_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))
    teacher_rel = relationship(Teacher)
    group_rel = relationship(Group)

class Points_table(Base):
    __tablename__ = 'Info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_info =   Column(Integer, ForeignKey('students.id', ondelete="CASCADE"))
    lesson_id =   Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"))
    points =   Column(Integer)
    date_of =  Column(Date)
    student_rel = relationship(Student)
    subject_rel = relationship(Subject)


