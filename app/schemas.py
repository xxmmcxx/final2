from pydantic import BaseModel, Field, validator
import os
import json
from .database import SessionLocal
from . import crud

db = SessionLocal()

persian_char = [" ", "ا", "آ", "ب", "پ", "ت", "ث", "ج", "چ", "خ", "ح", "د", "ذ", "ر", "ز", "ژ", "ئ", "س", "ش", "ص",
                "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ک", "گ", "ل", "م", "ن", "و", "ه", "ي", "ك", "ء", "ی"]
departments = ["فنی و مهندسی", "علوم پایه", "علوم انسانی", "دامپزشکی", "اقتصاد", "کشاورزی", "منابع طبیعی"]
majors = ["برق", "کامپیوتر", "عمران", "مکانیک", "معدن", "شهرسازی", "صنایع", "شیمی", "مواد", "هوافضا", "معماری"]

class Prof(BaseModel):
    pk: int
    lid: int
    fname: str
    lname: str
    id: str
    dept: str
    major: str
    birth: str
    born_city: str
    address: str = Field(max_length=100)
    postal_code: str = Field(pattern=r"^[0-9]{10}$")
    cphone: str = Field(pattern=r"^((\+98|0|098)9\d{9})$")
    hphone: str = Field(pattern=r"^0[1|3|4|5|6|7|8|9][0-9]{9}$|^02[0-9]{9}$")
    lesson_ids: str

    @validator("lid")
    def validate_lid(cls, value):
        if len(str(value)) != 6:
            raise ValueError("LID must be 6 digits.")
        return value

    @validator("fname")
    def validate_fname(cls, value):
        if len(value) > 10:
            raise ValueError("First name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("First name must only contain Persian characters")
        return value

    @validator("lname")
    def validate_lname(cls, value):
        if len(value) > 10:
            raise ValueError("Last name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("Last name must only contain Persian characters")
        return value

    @validator("id")
    def validate_meli_code(cls, value):
        value = str(value)
        if len(value) != 10:
            raise ValueError("National code is not correct.")

        res = sum(int(num) * (10 - i) for i, num in enumerate(value[:-1]))
        remain = res % 11
        if remain < 2:
            if remain != int(value[-1]):
                raise ValueError("National code is not correct.")
        else:
            if (11 - remain) != int(value[-1]):
                raise ValueError("National code is not correct.")

        return value

    @validator("dept")
    def validate_dept(cls, value):
        if value not in departments:
            raise ValueError("Department is not correct.")
        return value

    @validator("major")
    def validate_major(cls, value):
        if value not in majors:
            raise ValueError("Major is not correct.")
        return value

    @validator("birth")
    def validate_birth(cls, value):
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError("Date format is not correct.")
        year, month, day = map(int, value.split("-"))
        if not 1300 < year < 1403:
            raise ValueError("Year is not correct.")
        if not 1 <= month <= 12:
            raise ValueError("Month is not correct.")
        if not 1 <= day <= 31:
            raise ValueError("Day is not correct.")
        return value

    @validator("born_city")
    def validate_born_city(cls, value):
        with open('project/data/cities.json', 'r', encoding="utf-8") as json_file:
            cities = json.load(json_file)
        city_names = [c["name"] for c in cities]

        if value not in city_names:
            raise ValueError("City is not correct.")
        return value

    @validator("lesson_ids")
    def validate_lesson_ids(cls, value):
        try:
            lessons = value.split(",")
            for lesson in lessons:
                a = int(lesson)
        except:
            raise ValueError("Courses IDs must be separated by commas")

        for lesson in lessons:
            lesson = crud.get_lesson(db, int(lesson))
            if lesson is None:
                raise ValueError("Course ID is not correct!")
        return value

class Les(BaseModel):
    pk: int
    c_id: int
    cname: str
    dept: str
    credit: int = Field(ge=1, le=4)

    @validator("c_id")
    def validate_cid(cls, value):
        if len(str(value)) != 5:
            raise ValueError("CID must be 5 digits.")
        return value

    @validator("cname")
    def validate_cname(cls, value):
        if len(value) > 25:
            raise ValueError("Course name is too long (must be less than 25 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("Course name must only contain Persian characters")
        return value

    @validator("dept")
    def validate_dept(cls, value):
        if value not in departments:
            raise ValueError("Department is not correct.")
        return value

class Stu(BaseModel):
    pk: int
    stid: int
    fname: str
    lname: str
    father: str
    birth: str
    ids: str
    born_city: str
    address: str = Field(max_length=100)
    postal_code: str = Field(pattern=r"^[0-9]{10}$")
    cphone: str = Field(pattern=r"^((\+98|0|098)9\d{9})$")
    hphone: str = Field(pattern=r"^0[1|3|4|5|6|7|8|9][0-9]{9}$|^02[0-9]{9}$")
    dept: str
    major: str
    married: bool
    id: str
    course_ids: str
    prof_ids: str
    s_course_ids: list[Les] = []
    lids: list[Prof] = []

    @validator("stid")
    def validate_stid(cls, value):
        if len(str(value)) != 11:
            raise ValueError("Student code should be 11 digits!")
        year = int(str(value)[:3])
        if not 400 <= year <= 403:
            raise ValueError("Year part is not correct!")
        if int(str(value)[3:9]) != 114150:
            raise ValueError("Middle part is not correct!")
        if not 1 <= int(str(value)[-2:]) <= 99:
            raise ValueError("Index is not correct!")
        return value

    @validator("fname")
    def validate_fname(cls, value):
        if len(value) > 10:
            raise ValueError("First name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("First name must only contain Persian characters")
        return value

    @validator("lname")
    def validate_lname(cls, value):
        if len(value) > 10:
            raise ValueError("Last name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("Last name must only contain Persian characters")
        return value

    @validator("father")
    def validate_father(cls, value):
        if len(value) > 10:
            raise ValueError("Father's name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("Father's name must only contain Persian characters")
        return value

    @validator("birth")
    def validate_birth(cls, value):
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError("Date format is not correct.")
        year, month, day = map(int, value.split("-"))
        if not 1300 < year < 1403:
            raise ValueError("Year is not correct.")
        if not 1 <= month <= 12:
            raise ValueError("Month is not correct.")
        if not 1 <= day <= 31:
            raise ValueError("Day is not correct.")
        return value

    @validator("ids")
    def validate_ids(cls, value):
        if len(value) != 10 or value[0] not in persian_char or value[3] != "/":
            raise ValueError("The format of serial is not correct.")
        try:
            a = int(value[1:3])
            b = int(value[4:])
        except:
            raise ValueError("The format of serial is not correct.")
        return value

    @validator("born_city")
    def validate_born_city(cls, value):
        with open('project/data/cities.json', 'r', encoding="utf-8") as json_file:
            cities = json.load(json_file)
        city_names = [c["name"] for c in cities]

        if value not in city_names:
            raise ValueError("City is not correct.")
        return value

    @validator("dept")
    def validate_dept(cls, value):
        if value not in departments:
            raise ValueError("Department is not correct.")
        return value

    @validator("major")
    def validate_major(cls, value):
        if value not in majors:
            raise ValueError("Major is not correct.")
        return value

    @validator("id")
    def validate_meli_code(cls, value):
        value = str(value)
        if len(value) != 10:
            raise ValueError("National code is not correct.")

        res = sum(int(num) * (10 - i) for i, num in enumerate(value[:-1]))
        remain = res % 11
        if remain < 2:
            if remain != int(value[-1]):
                raise ValueError("National code is not correct.")
        else:
            if (11 - remain) != int(value[-1]):
                raise ValueError("National code is not correct.")

        return value

    @validator("course_ids")
    def validate_course_ids(cls, value):
        try:
            lessons = value.split(",")
            for lesson in lessons:
                a = int(lesson)
        except:
            raise ValueError("Courses IDs must be separated by commas")

        for lesson in lessons:
            lesson = crud.get_lesson(db, int(lesson))
            if lesson is None:
                raise ValueError("Course ID is not correct!")
        return value

    @validator("prof_ids")
    def validate_prof_ids(cls, value):
        try:
            professors = value.split(",")
            for professor in professors:
                a = int(professor)
        except:
            raise ValueError("Professors IDs must be separated by commas")

        for professor in professors:
            professor = crud.get_professor(db, int(professor))
            if professor is None:
                raise ValueError("Professor ID is not correct!")
        return value
