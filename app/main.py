from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# student

@app.get("/students/")
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.get("/students/{student_id}/")
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.post("/RegStu/")
def create_student(student: schemas.Student, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, id=student.STID)
    if db_student:
        raise HTTPException(status_code=400, detail="student already registered")
    return crud.create_student(db=db, student=student)

@app.delete("/DelStu/{STID}/")
def delete_student(STID: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, id=STID)
    if not db_student:
        raise HTTPException(status_code=400, detail="student not exist")
    return crud.delete_student(db=db, id=STID)

@app.put("/UpdateStu/{STID}/")
async def update_student(STID: int, student: schemas.Student, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, id=STID)
    if not db_student:
        raise HTTPException(status_code=400, detail="student not exist")
    return crud.update_student(db=db, id=STID, student=student)



# professor

@app.get("/professors/")
def read_professors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    professors = crud.get_professors(db, skip=skip, limit=limit)
    return professors

@app.get("/professors/{professo_id}/")
def read_professor(professo_id: int, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, id=professo_id)
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return db_professor

@app.post("/RegPro/")
def create_professor(professor: schemas.Professor, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, id=professor.LID)
    if db_professor:
        raise HTTPException(status_code=400, detail="Professor already registered")
    return crud.create_professor(db=db, professor=professor)

@app.delete("/DelPro/{LID}/")
def delete_professor(LID: int, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, id=LID)
    if not db_professor:
        raise HTTPException(status_code=400, detail="Professor not exist")
    return crud.delete_professor(db=db, id=LID)

@app.put("/UpdatePro/{LID}/")
async def update_professor(LID: int, professor: schemas.Professor, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, id=LID)
    if not db_professor:
        raise HTTPException(status_code=400, detail="Professor not exist")
    return crud.update_professor(db=db, id=LID, professor=professor)



# lesson

@app.get("/lessons/")
def read_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lessons = crud.get_lessons(db, skip=skip, limit=limit)
    return lessons

@app.get("/lessons/{lesson_id}/")
def read_lesson(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson

@app.post("/RegLesson/")
def create_lesson(lesson: schemas.Lesson, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, id=lesson.CID)
    if db_lesson:
        raise HTTPException(status_code=400, detail="Lesson already registered")
    return crud.create_lesson(db=db, lesson=lesson)

@app.delete("/DelLesson/{CID}/")
def delete_lesson(CID: int, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, id=CID)
    if not db_lesson:
        raise HTTPException(status_code=400, detail="Lesson not exist")
    return crud.delete_lesson(db=db, id=CID)

@app.put("/UpdateLesson/{CID}/")
async def update_lesson(CID: int, lesson: schemas.Lesson, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, id=CID)
    if not db_lesson:
        raise HTTPException(status_code=400, detail="Lesson not exist")
    return crud.update_lesson(db=db, id=CID, lesson=lesson)

