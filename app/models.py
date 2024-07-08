from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base

stu_les_assoc = Table(
    'stu_les',
    Base.metadata,
    Column('stu_id', Integer, ForeignKey('stus.stid')),
    Column('les_id', Integer, ForeignKey('less.c_id'))
)

stu_prof_assoc = Table(
    'stu_prof',
    Base.metadata,
    Column('stu_id', Integer, ForeignKey('stus.stid')),
    Column('prof_id', Integer, ForeignKey('profs.lid'))
)

prof_les_assoc = Table(
    'prof_les',
    Base.metadata,
    Column('prof_id', Integer, ForeignKey('profs.lid')),
    Column('les_id', Integer, ForeignKey('less.c_id'))
)

class Stu(Base):
    __tablename__ = "stus"
    pk = Column(Integer, primary_key=True, unique=True, index=True)
    stid = Column(Integer, unique=True)
    fname = Column(String)
    lname = Column(String)
    father = Column(String)
    birth = Column(String)
    ids = Column(String)
    born_city = Column(String)
    address = Column(String)
    postal_code = Column(String)
    cphone = Column(String)
    hphone = Column(String)
    dept = Column(String)
    major = Column(String)
    married = Column(Boolean)
    id = Column(String, unique=True)
    c_ids = Column(String)
    p_ids = Column(String)

    s_c_ids = relationship("Les", secondary=stu_les_assoc, back_populates="stu")
    lids = relationship("Prof", secondary=stu_prof_assoc, back_populates="stu")


class Prof(Base):
    __tablename__ = "profs"
    pk = Column(Integer, primary_key=True, unique=True)
    lid = Column(Integer, unique=True)
    fname = Column(String)
    lname = Column(String)
    id = Column(String, unique=True)
    dept = Column(String)
    major = Column(String)
    birth = Column(String)
    born_city = Column(String)
    address = Column(String)
    postal_code = Column(String)
    cphone = Column(String)
    hphone = Column(String)
    l_ids = Column(String)

    l_c_ids = relationship("Les", secondary=prof_les_assoc, back_populates="prof")
    stu = relationship("Stu", secondary=stu_prof_assoc, back_populates="lids")


class Les(Base):
    __tablename__ = "less"
    pk = Column(Integer, primary_key=True, unique=True)
    c_id = Column(Integer, unique=True)
    cname = Column(String)
    dept = Column(String)
    credit = Column(Integer)

    stu = relationship("Stu", secondary=stu_les_assoc, back_populates="s_c_ids")
    prof = relationship("Prof", secondary=prof_les_assoc, back_populates="l_c_ids")
