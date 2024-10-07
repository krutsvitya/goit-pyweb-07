from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random

from database import Base, Student, Group, Teacher, Subject, Grade

fake = Faker()

engine = create_engine('postgresql://postgres:091003@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()


def seed_data():
    groups = []
    for _ in range(3):
        group = Group()
        groups.append(group)

    session.add_all(groups)
    session.commit()

    teachers = []
    for _ in range(random.randint(3, 5)):
        teacher = Teacher(name=fake.name())
        teachers.append(teacher)

    session.add_all(teachers)
    session.commit()

    subjects = []
    for _ in range(random.randint(5, 8)):
        subject = Subject(name=fake.word(), teacher_id=random.choice(teachers).teacher_id)
        subjects.append(subject)

    session.add_all(subjects)
    session.commit()

    students = []
    for _ in range(random.randint(30, 50)):
        student = Student(name=fake.name(), group_id=random.choice(groups).group_id)
        students.append(student)

    session.add_all(students)
    session.commit()

    grades = []
    for student in students:
        for _ in range(random.randint(5, 20)):
            grade = Grade(
                student_id=student.id,
                subject_id=random.choice(subjects).sub_id,
                grade=random.uniform(2.0, 5.0),
                date_received=fake.date_between(start_date='-1y', end_date='today')
            )
            grades.append(grade)

    session.add_all(grades)
    session.commit()

    print("База даних успішно заповнена випадковими даними.")


if __name__ == "__main__":
    seed_data()

session.close()

