from sqlalchemy.orm import Session
from . import models, schemas

def set_les(db, table, lessons):
    for les in lessons:
        les = get_les(db, int(les))
        table.SCourseIDs.append(les)

def set_prof(db, table, profs):
    for prof in profs:
        prof = get_prof(db, int(prof))
        table.LIDs.append(prof)

def set_prof_les(db, table, lessons):
    for les in lessons:
        les = get_les(db, int(les))
        table.LCourseIDs.append(les)

# stu

def get_stu(db: Session, id: int):
    return db.query(models.Student).filter(models.Student.STID == id).first()

def get_stus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_stu(db: Session, stu: schemas.Stu):
    db_stu = models.Student(pk=stu.pk, STID=stu.STID, Fname=stu.Fname, Lname=stu.Lname, Father=stu.Father, Birth=stu.Birth, IDS=stu.IDS, BornCity=stu.BornCity, Address=stu.Address, PostalCode=stu.PostalCode, CPhone=stu.CPhone, HPhone=stu.HPhone, Department=stu.Department, Major=stu.Major, Married=stu.Married, ID=stu.ID, Courses_ids=stu.Courses_ids, Professor_ids=stu.Professor_ids)

    set_les(db, db_stu, stu.Courses_ids.split(","))
    set_prof(db, db_stu, stu.Professor_ids.split(","))

    db.add(db_stu)
    db.commit()
    db.refresh(db_stu)
    return db_stu

def delete_stu(db: Session, id: int):
    db_stu = db.query(models.Student).filter(models.Student.STID == id).first()
    name = f"{db_stu.Fname} {db_stu.Lname}"
    db.delete(db_stu)
    db.commit()
    return {"message": f"the student {name} deleted successfully."}

def update_stu(db: Session, id: int, stu: schemas.Stu):
    db_stu = db.query(models.Student).filter(models.Student.STID == id).first()
    db_stu.Fname = stu.Fname
    db_stu.Lname = stu.Lname
    db_stu.Father = stu.Father
    db_stu.Birth = stu.Birth
    db_stu.IDS = stu.IDS
    db_stu.BornCity = stu.BornCity
    db_stu.Address = stu.Address
    db_stu.PostalCode = stu.PostalCode
    db_stu.CPhone = stu.CPhone
    db_stu.HPhone = stu.HPhone
    db_stu.Department = stu.Department
    db_stu.Major = stu.Major
    db_stu.Married = stu.Married
    db_stu.ID = stu.ID
    db_stu.Courses_ids = stu.Courses_ids
    db_stu.Professor_ids = stu.Professor_ids

    db_stu.SCourseIDs = []
    db_stu.LIDs = []
    set_les(db, db_stu, stu.Courses_ids.split(","))
    set_prof(db, db_stu, stu.Professor_ids.split(","))

    db.commit()
    return {"message": f"the student {db_stu.STID} updated successfully."}

# prof

def get_prof(db: Session, id: int):
    return db.query(models.Professor).filter(models.Professor.LID == id).first()

def get_profs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Professor).offset(skip).limit(limit).all()

def create_prof(db: Session, prof: schemas.Prof):
    db_prof = models.Professor(pk=prof.pk, LID=prof.LID, Fname=prof.Fname, Lname=prof.Lname, ID=prof.ID, Department=prof.Department, Major=prof.Major, Birth=prof.Birth, BornCity=prof.BornCity, Address=prof.Address, PostalCode=prof.PostalCode, CPhone=prof.CPhone, HPhone=prof.HPhone, Lesson_ids=prof.Lesson_ids)

    set_prof_les(db, db_prof, prof.Lesson_ids.split(","))

    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)
    return db_prof

def delete_prof(db: Session, id: int):
    db_prof = db.query(models.Professor).filter(models.Professor.LID == id).first()
    name = f"{db_prof.Fname} {db_prof.Lname}"
    db.delete(db_prof)
    db.commit()
    return {"message": f"the professor {name} deleted successfully."}

def update_prof(db: Session, id: int, prof: schemas.Prof):
    db_prof = db.query(models.Professor).filter(models.Professor.LID == id).first()
    db_prof.Fname = prof.Fname
    db_prof.Lname = prof.Lname
    db_prof.ID = prof.ID
    db_prof.Department = prof.Department
    db_prof.Major = prof.Major
    db_prof.Birth = prof.Birth
    db_prof.BornCity = prof.BornCity
    db_prof.Address = prof.Address
    db_prof.PostalCode = prof.PostalCode
    db_prof.CPhone = prof.CPhone
    db_prof.HPhone = prof.HPhone
    db_prof.Lesson_ids = prof.Lesson_ids

    db_prof.LCourseIDs = []
    set_prof_les(db, db_prof, prof.Lesson_ids.split(","))

    db.commit()
    return {"message": f"the professor {db_prof.LID} updated successfully."}

# les

def get_les(db: Session, id: int):
    return db.query(models.Lesson).filter(models.Lesson.CID == id).first()

def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lesson).offset(skip).limit(limit).all()

def create_les(db: Session, les: schemas.Les):
    db_les = models.Lesson(pk=les.pk, CID=les.CID, CName=les.CName, Department=les.Department, Credit=les.Credit)
    db.add(db_les)
    db.commit()
    db.refresh(db_les)
    return db_les

def delete_les(db: Session, id: int):
    db_les = db.query(models.Lesson).filter(models.Lesson.CID == id).first()
    db.delete(db_les)
    db.commit()
    return {"message": f"the lesson {db_les.CName} deleted successfully."}

def update_les(db: Session, id: int, les: schemas.Les):
    db_les = db.query(models.Lesson).filter(models.Lesson.CID == id).first()
    db_les.CName = les.CName
    db_les.Department = les.Department
    db_les.Credit = les.Credit

    db.commit()
    return {"message": f"the lesson {db_les.CID} updated successfully."}