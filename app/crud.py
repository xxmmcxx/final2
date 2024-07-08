from sqlalchemy.orm import Session
from . import models, schemas

def set_lesson(db, table, lessons):
    for lesson in lessons:
        lesson = get_lesson(db, int(lesson))
        table.SCourseIDs.append(lesson)

def set_professor(db, table, professors):
    for professor in professors:
        professor = get_professor(db, int(professor))
        table.LIDs.append(professor)

def set_professor_lesson(db, table, lessons):
    for lesson in lessons:
        lesson = get_lesson(db, int(lesson))
        table.LCourseIDs.append(lesson)



# student

def get_student(db: Session, id: int):
    return db.query(models.Student).filter(models.Student.STID == id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.Student):
    db_student = models.Student(pk=student.pk, STID=student.STID, Fname=student.Fname, Lname=student.Lname, Father=student.Father, Birth=student.Birth, IDS=student.IDS, BornCity=student.BornCity, Address=student.Address, PostalCode=student.PostalCode, CPhone=student.CPhone, HPhone=student.HPhone, Department=student.Department,  Major=student.Major,  Married=student.Married, ID=student.ID, Courses_ids=student.Courses_ids, Professor_ids=student.Professor_ids)

    set_lesson(db, db_student, student.Courses_ids.split(","))
    set_professor(db, db_student, student.Professor_ids.split(","))

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, id: int):
    db_student = db.query(models.Student).filter(models.Student.STID == id).first()
    name = f"{db_student.Fname} {db_student.Lname}"
    db.delete(db_student)
    db.commit()
    return {"message" : f"the student {name} deleted successfully."}

def update_student(db: Session, id: int, student: schemas.Student):
    db_student = db.query(models.Student).filter(models.Student.STID == id).first()
    db_student.Fname = student.Fname
    db_student.Lname = student.Lname
    db_student.Father = student.Father
    db_student.Birth = student.Birth
    db_student.IDS = student.IDS
    db_student.BornCity = student.BornCity
    db_student.Address = student.Address
    db_student.PostalCode = student.PostalCode
    db_student.CPhone = student.CPhone
    db_student.HPhone = student.HPhone
    db_student.Department = student.Department
    db_student.Major = student.Major
    db_student.Married = student.Married
    db_student.ID = student.ID
    db_student.Courses_ids = student.Courses_ids
    db_student.Professor_ids = student.Professor_ids

    db_student.SCourseIDs = []
    db_student.LIDs = []
    set_lesson(db, db_student, student.Courses_ids.split(","))
    set_professor(db, db_student, student.Professor_ids.split(","))

    db.commit()
    return {"message" : f"the student {db_student.STID} updated successfully."}



# professor

def get_professor(db: Session, id: int):
    return db.query(models.Professor).filter(models.Professor.LID == id).first()

def get_professors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Professor).offset(skip).limit(limit).all()

def create_professor(db: Session, professor: schemas.Professor):
    db_professor = models.Professor(pk=professor.pk, LID=professor.LID, Fname=professor.Fname, Lname=professor.Lname, ID=professor.ID, Department=professor.Department, Major=professor.Major, Birth=professor.Birth, BornCity=professor.BornCity, Address=professor.Address, PostalCode=professor.PostalCode, CPhone=professor.CPhone, HPhone=professor.HPhone, Lesson_ids=professor.Lesson_ids)

    set_professor_lesson(db, db_professor, professor.Lesson_ids.split(","))

    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def delete_professor(db: Session, id: int):
    db_professor = db.query(models.Professor).filter(models.Professor.LID == id).first()
    name = f"{db_professor.Fname} {db_professor.Lname}"
    db.delete(db_professor)
    db.commit()
    return {"message" : f"the professor {name} deleted successfully."}

def update_professor(db: Session, id: int, professor: schemas.Professor):
    db_professor = db.query(models.Professor).filter(models.Professor.LID == id).first()
    db_professor.Fname = professor.Fname
    db_professor.Lname = professor.Lname
    db_professor.ID = professor.ID
    db_professor.Department = professor.Department
    db_professor.Major = professor.Major
    db_professor.Birth = professor.Birth
    db_professor.BornCity = professor.BornCity
    db_professor.Address = professor.Address
    db_professor.PostalCode = professor.PostalCode
    db_professor.CPhone = professor.CPhone
    db_professor.HPhone = professor.HPhone
    db_professor.Lesson_ids = professor.Lesson_ids

    db_professor.LCourseIDs = []
    set_professor_lesson(db, db_professor, professor.Lesson_ids.split(","))

    db.commit()
    return {"message" : f"the professor {db_professor.LID} updated successfully."}



# lesson

def get_lesson(db: Session, id: int):
    return db.query(models.Lesson).filter(models.Lesson.CID == id).first()

def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lesson).offset(skip).limit(limit).all()

def create_lesson(db: Session, lesson: schemas.Lesson):
    db_lesson = models.Lesson(pk=lesson.pk, CID=lesson.CID, CName=lesson.CName, Department=lesson.Department, Credit=lesson.Credit)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def delete_lesson(db: Session, id: int):
    db_lesson = db.query(models.Lesson).filter(models.Lesson.CID == id).first()
    db.delete(db_lesson)
    db.commit()
    return {"message" : f"the lesson {db_lesson.CName} deleted successfully."}

def update_lesson(db: Session, id: int, lesson: schemas.Lesson):
    db_lesson = db.query(models.Lesson).filter(models.Lesson.CID == id).first()
    db_lesson.CName = lesson.CName
    db_lesson.Department = lesson.Department
    db_lesson.Credit = lesson.Credit

    db.commit()
    return {"message" : f"the lesson {db_lesson.CID} updated successfully."}


