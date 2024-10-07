from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    group = relationship("Group")


class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)


class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    sub_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'))
    teacher = relationship("Teacher")


class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.sub_id'))
    grade = Column(Float, nullable=False)
    date_received = Column(Date, default=datetime.date.today)

    student = relationship("Student")
    subject = relationship("Subject")


engine = create_engine('postgresql://postgres:091003@localhost:5432/postgres')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
