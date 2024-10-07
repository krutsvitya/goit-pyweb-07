from sqlalchemy import func, desc, create_engine, cast, Numeric
from sqlalchemy.orm import sessionmaker
from database import Student, Grade, Subject, Teacher, Group, Base


engine = create_engine('postgresql://postgres:091003@localhost:5432/postgres')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    results = session.query(
        Student.name,
        func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')
    ).select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

    return [(student_name, float(avg_grade)) for student_name, avg_grade in results]

def select_2(subject_id):
    result = session.query(
        Student.name.label("students_name"),
        func.round(func.avg(cast(Grade.grade, Numeric)), 2).label("avg_grade")
    ).select_from(Grade).join(Student).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(
        desc('avg_grade')).first()

    # Конвертація Decimal в float
    if result:
        students_name, avg_grade = result
        return students_name, float(avg_grade)  # Конвертуємо в float
    return None

def select_3(subject_id):
    result = session.query(
        Group.group_id,
        func.round(func.avg(cast(Grade.grade, Numeric)), 2).label("avg_grade")
    ).select_from(Grade).join(Student).join(Group).filter(Grade.subject_id == subject_id).group_by(Group.group_id).all()

    # Если результат не пустой, вернуть все группы и их средние оценки
    if result:
        return [(group_id, float(avg_grade)) for group_id, avg_grade in result]
    return None


def select_4():
    return session.query(
        func.round(func.avg(Grade.grade).cast(Numeric), 2).label("avg_grade")
    ).scalar()


def select_5(teacher_id):
    return session.query(
        Subject.name
    ).filter(Subject.teacher_id == teacher_id).all()


def select_6(group_id):
    return session.query(
        Student.name
    ).join(Group).filter(Group.group_id == group_id).all()


def select_7(group_id, subject_id):
    return session.query(
        Student.name,
        Grade.grade
    ).select_from(Grade).join(Student).join(Group).filter(Group.group_id == group_id, Grade.subject_id == subject_id).all()


def select_8(teacher_id):
    return session.query(
        func.round(func.avg(cast(Grade.grade, Numeric)), 2).label('avg_grade')
    ).select_from(Grade).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()


def select_9(student_id):
    return session.query(
        Subject.name
    ).join(Grade).join(Student).filter(Student.id == student_id).distinct().all()


def select_10(student_id, teacher_id):
    return session.query(
        Subject.name
    ).filter(
        Subject.teacher_id == teacher_id,
        Subject.sub_id.in_(
            session.query(Grade.subject_id)
            .filter(Grade.student_id == student_id)
        )
    ).distinct().all()  # Используем distinct, чтобы убрать дубликаты
  # Извлекаем только значения из кортежей

print(select_1())
print(select_2(2))
print(select_3(5))
print(select_4())
print(select_5(3))
print(select_6(2))
print(select_7(1, 4))
print(select_8(1))
print(select_9(25))
print(select_10(34, 2))


