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

# stu (student)

@app.get("/students/")
def read_stus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stus = crud.get_stus(db, skip=skip, limit=limit)
    return stus

@app.get("/students/{stu_id}/")
def read_stu(stu_id: int, db: Session = Depends(get_db)):
    db_stu = crud.get_stu(db, id=stu_id)
    if db_stu is None:
        raise HTTPException(status_code=404, detail="Stu not found")
    return db_stu

@app.post("/RegStu/")
def create_stu(stu: schemas.Stu, db: Session = Depends(get_db)):
    db_stu = crud.get_stu(db, id=stu.STID)
    if db_stu:
        raise HTTPException(status_code=400, detail="Stu already registered")
    return crud.create_stu(db=db, stu=stu)

@app.delete("/DelStu/{STID}/")
def delete_stu(STID: int, db: Session = Depends(get_db)):
    db_stu = crud.get_stu(db, id=STID)
    if not db_stu:
        raise HTTPException(status_code=400, detail="Stu not exist")
    return crud.delete_stu(db=db, id=STID)

@app.put("/UpdateStu/{STID}/")
async def update_stu(STID: int, stu: schemas.Stu, db: Session = Depends(get_db)):
    db_stu = crud.get_stu(db, id=STID)
    if not db_stu:
        raise HTTPException(status_code=400, detail="Stu not exist")
    return crud.update_stu(db=db, id=STID, stu=stu)

# prof (professor)

@app.get("/professors/")
def read_profs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profs = crud.get_profs(db, skip=skip, limit=limit)
    return profs

@app.get("/professors/{prof_id}/")
def read_prof(prof_id: int, db: Session = Depends(get_db)):
    db_prof = crud.get_prof(db, id=prof_id)
    if db_prof is None:
        raise HTTPException(status_code=404, detail="Prof not found")
    return db_prof

@app.post("/RegProf/")
def create_prof(prof: schemas.Prof, db: Session = Depends(get_db)):
    db_prof = crud.get_prof(db, id=prof.LID)
    if db_prof:
        raise HTTPException(status_code=400, detail="Prof already registered")
    return crud.create_prof(db=db, prof=prof)

@app.delete("/DelProf/{LID}/")
def delete_prof(LID: int, db: Session = Depends(get_db)):
    db_prof = crud.get_prof(db, id=LID)
    if not db_prof:
        raise HTTPException(status_code=400, detail="Prof not exist")
    return crud.delete_prof(db=db, id=LID)

@app.put("/UpdateProf/{LID}/")
async def update_prof(LID: int, prof: schemas.Prof, db: Session = Depends(get_db)):
    db_prof = crud.get_prof(db, id=LID)
    if not db_prof:
        raise HTTPException(status_code=400, detail="Prof not exist")
    return crud.update_prof(db=db, id=LID, prof=prof)

# les (lesson)

@app.get("/lessons/")
def read_les(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    les = crud.get_les(db, skip=skip, limit=limit)
    return les

@app.get("/lessons/{les_id}/")
def read_le(les_id: int, db: Session = Depends(get_db)):
    db_le = crud.get_le(db, id=les_id)
    if db_le is None:
        raise HTTPException(status_code=404, detail="Les not found")
    return db_le

@app.post("/RegLes/")
def create_le(le: schemas.Les, db: Session = Depends(get_db)):
    db_le = crud.get_le(db, id=le.CID)
    if db_le:
        raise HTTPException(status_code=400, detail="Les already registered")
    return crud.create_le(db=db, le=le)

@app.delete("/DelLes/{CID}/")
def delete_le(CID: int, db: Session = Depends(get_db)):
    db_le = crud.get_le(db, id=CID)
    if not db_le:
        raise HTTPException(status_code=400, detail="Les not exist")
    return crud.delete_le(db=db, id=CID)

@app.put("/UpdateLes/{CID}/")
async def update_le(CID: int, le: schemas.Les, db: Session = Depends(get_db)):
    db_le = crud.get_le(db, id=CID)
    if not db_le:
        raise HTTPException(status_code=400, detail="Les not exist")
    return crud.update_le(db=db, id=CID, le=le)
