from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base


student_lesson_association = Table(
    'student_lesson',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.STID')),
    Column('lesson_id', Integer, ForeignKey('lessons.CID'))
)

student_professor_association = Table(
    'student_professor',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.STID')),
    Column('professor_id', Integer, ForeignKey('professors.LID'))
)

professor_lesson_association = Table(
    'professor_lesson',
    Base.metadata,
    Column('professor_id', Integer, ForeignKey('professors.LID')),
    Column('lesson_id', Integer, ForeignKey('lessons.CID'))
)

class Student(Base):
    __tablename__ = "students"
    pk = Column(Integer, primary_key=True, unique=True, index=True)
    STID = Column(Integer, unique=True)
    Fname = Column(String)
    Lname = Column(String)
    Father = Column(String)
    Birth = Column(String)
    IDS = Column(String)
    BornCity = Column(String)
    Address = Column(String)
    PostalCode = Column(String)
    CPhone = Column(String)
    HPhone = Column(String)
    Department = Column(String)
    Major = Column(String)
    Married = Column(Boolean)
    ID = Column(String, unique=True)
    Courses_ids = Column(String)
    Professor_ids = Column(String)

    SCourseIDs = relationship("Lesson", secondary=student_lesson_association, back_populates="student")
    LIDs = relationship("Professor", secondary=student_professor_association, back_populates="student")



class Professor(Base):
    __tablename__ = "professors"
    pk = Column(Integer, primary_key=True, unique=True)
    LID = Column(Integer, unique=True)
    Fname = Column(String)
    Lname = Column(String)
    ID = Column(String, unique=True)
    Department = Column(String)
    Major = Column(String)
    Birth = Column(String)
    BornCity = Column(String)
    Address = Column(String)
    PostalCode = Column(String)
    CPhone = Column(String)
    HPhone = Column(String)
    Lesson_ids = Column(String)

    LCourseIDs = relationship("Lesson", secondary=professor_lesson_association, back_populates="professor")
    student = relationship("Student", secondary=student_professor_association, back_populates="LIDs")


class Lesson(Base):
    __tablename__ = "lessons"
    pk = Column(Integer, primary_key=True, unique=True)
    CID = Column(Integer, unique=True)
    CName = Column(String)
    Department = Column(String)
    Credit = Column(Integer)

    student = relationship("Student", secondary=student_lesson_association, back_populates="SCourseIDs")
    professor = relationship("Professor", secondary=professor_lesson_association, back_populates="LCourseIDs")


