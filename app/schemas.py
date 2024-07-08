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



class Professor(BaseModel):
    pk: int
    LID: int
    Fname: str
    Lname: str
    ID: str
    Department: str
    Major: str
    Birth: str
    BornCity: str
    Address: str = Field(max_length=100)
    PostalCode: str = Field(pattern=r"^[0-9]{10}$")
    CPhone: str = Field(pattern=r"^((\+98|0|098)9\d{9})$")
    HPhone: str = Field(pattern=r"^0[1|3|4|5|6|7|8|9][0-9]{9}$|^02[0-9]{9}$")
    Lesson_ids: str
    #LCourseIDs: list[Lesson] = []

    @validator("LID")
    def validate_LID(cls, value):
        if len(str(value)) != 6:
            raise ValueError("LID must be 6 digits.")
        return value


    @validator("Fname")
    def validate_Fname(cls, value):
        if len(value) > 10:
            raise ValueError("first name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("first name must be only contain persian characters")
        return value


    @validator("Lname")
    def validate_Lname(cls, value):
        if len(value) > 10:
            raise ValueError("last name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("last name must be only contain persian characters")
        return value


    @validator("ID")
    def validate_meli_code(cls, value):
        value = str(value)
        if not len(value) == 10:
            raise ValueError("national code is not correct.")

        res = 0
        for i, num in enumerate(value[:-1]):
            res = res + (int(num) * (10 - i))

        remain = res % 11
        if remain < 2:
            if not remain == int(value[-1]):
                raise ValueError("national code is not correct.")
        else:
            if not (11 - remain) == int(value[-1]):
                raise ValueError("national code is not correct.")

        return value


    @validator("Department")
    def validate_Department(cls, value):
        if value not in departments:
            raise ValueError("department is not correct.")
        return value

    @validator("Major")
    def validate_Major(cls, value):
        if value not in majors:
            raise ValueError("major is not correct.")
        return value


    @validator("Birth")
    def validate_Birth(cls, value):
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError("date format is not correct.")
        list = value.split("-")
        year = int(list[0])
        if not 1403 > year > 1300:
            raise ValueError("year is not correct.")
        month = int(list[1])
        if not 1 <= month <= 12:
            raise ValueError("month is not correct.")
        day = int(list[2])
        if not 1 <= day <= 31:
            raise ValueError("day is not correct.")
        return value


    @validator("BornCity")
    def validate_BornCity(cls, value):
        with open('project\data\cities.json', 'r', encoding="utf-8") as json_file:
            cities = json.load(json_file)
        cities = list(cities)
        new_cities = []
        for c in cities:
            new_cities.append(c["name"])

        if value not in new_cities:
            raise ValueError("city is not correct.")

        return value




    @validator("Lesson_ids")
    def validate_Lesson_ids(cls, value):
        try:
            lessons = value.split(",")
            for lesson in lessons:
                a = int(lesson)
        except:
            raise ValueError("Courses id must separate by ,")

        for lesson in lessons:
            lesson =  crud.get_lesson(db, int(lesson))
            if lesson is None:
                raise ValueError("Courses id is not correct!")

        return value


class Lesson(BaseModel):
    pk: int
    CID: int
    CName: str
    Department: str
    Credit: int = Field(ge=1, le=4)


    @validator("CID")
    def validate_CID(cls, value):
        if len(str(value)) != 5:
            raise ValueError("CID must be 5 digits.")
        return value


    @validator("CName")
    def validate_CName(cls, value):
        if len(value) > 25:
            raise ValueError("CID is too long (must be less than 25 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("CID must be only contain persian characters")
        return value


    @validator("Department")
    def validate_Department(cls, value):
        if value not in departments:
            raise ValueError("department is not correct.")
        return value


class Student(BaseModel):
    pk: int
    STID: int
    Fname: str
    Lname: str
    Father: str
    Birth: str
    IDS: str
    BornCity: str
    Address: str = Field(max_length=100)
    PostalCode: str = Field(pattern=r"^[0-9]{10}$")
    CPhone: str = Field(pattern=r"^((\+98|0|098)9\d{9})$")
    HPhone: str = Field(pattern=r"^0[1|3|4|5|6|7|8|9][0-9]{9}$|^02[0-9]{9}$")
    Department: str
    Major: str
    Married: bool
    ID: str
    Courses_ids: str
    Professor_ids: str
    SCourseIDs: list[Lesson] = []
    LIDs: list[Professor] = []


    @validator("STID")
    def validate_STID(cls, value):
        if len(str(value)) != 11:
            raise ValueError("student code should be 11 digits!")
        year = int(str(value)[:3])
        if not 400 <= year <= 403:
            raise ValueError("year part is not correct!")
        middle = int(str(value)[3:9])
        if middle != 114150:
            raise ValueError("middle part is not correct!")
        index = int(str(value)[-2:])
        if not 1 <= index <= 99:
            raise ValueError("index is not correct!")
        return value



    @validator("Fname")
    def validate_Fname(cls, value):
        if len(value) > 10:
            raise ValueError("first name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("first name must be only contain persian characters")
        return value


    @validator("Lname")
    def validate_Lname(cls, value):
        if len(value) > 10:
            raise ValueError("last name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("last name must be only contain persian characters")
        return value


    @validator("Father")
    def validate_Father(cls, value):
        if len(value) > 10:
            raise ValueError("Father name is too long (must be less than 10 characters)")
        for i in value:
            if i not in persian_char:
                raise ValueError("Father name must be only contain persian characters")
        return value


    @validator("Birth")
    def validate_Birth(cls, value):
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError("date format is not correct.")
        list = value.split("-")
        year = int(list[0])
        if not 1403 > year > 1300:
            raise ValueError("year is not correct.")
        month = int(list[1])
        if not 1 <= month <= 12:
            raise ValueError("month is not correct.")
        day = int(list[2])
        if not 1 <= day <= 31:
            raise ValueError("day is not correct.")
        return value


    @validator("IDS")
    def validate_IDS(cls, value):
        if len(value) != 10 or value[0] not in persian_char or value[3] != "/" :
            raise ValueError("the format of serial is not correct.")
        try:
            a = int(value[1:3])
            b = int(value[4:])
        except:
            raise ValueError("the format of serial is not correct.")
        return value


    @validator("BornCity")
    def validate_BornCity(cls, value):
        with open('project\data\cities.json', 'r', encoding="utf-8") as json_file:
            cities = json.load(json_file)
        cities = list(cities)
        new_cities = []
        for c in cities:
            new_cities.append(c["name"])

        if value not in new_cities:
            raise ValueError("city is not correct.")

        return value



    @validator("Department")
    def validate_Department(cls, value):
        if value not in departments:
            raise ValueError("department is not correct.")
        return value

    @validator("Major")
    def validate_Major(cls, value):
        if value not in majors:
            raise ValueError("major is not correct.")
        return value


    @validator("ID")
    def validate_meli_code(cls, value):
        value = str(value)
        if not len(value) == 10:
            raise ValueError("national code is not correct.")

        res = 0
        for i, num in enumerate(value[:-1]):
            res = res + (int(num) * (10 - i))

        remain = res % 11
        if remain < 2:
            if not remain == int(value[-1]):
                raise ValueError("national code is not correct.")
        else:
            if not (11 - remain) == int(value[-1]):
                raise ValueError("national code is not correct.")

        return value


    @validator("Courses_ids")
    def validate_Courses_ids(cls, value):
        try:
            lessons = value.split(",")
            for lesson in lessons:
                a = int(lesson)
        except:
            raise ValueError("Courses id must separate by ,")

        for lesson in lessons:
            lesson =  crud.get_lesson(db, int(lesson))
            if lesson is None:
                raise ValueError("Courses id is not correct!")

        return value


    @validator("Professor_ids")
    def validate_Professor_ids(cls, value):
        try:
            professors = value.split(",")
            for professor in professors:
                a = int(professor)
        except:
            raise ValueError("Professors id must separate by ,")

        for professor in professors:
            professor =  crud.get_professor(db, int(professor))
            if professor is None:
                raise ValueError("Professor id is not correct!")

        return value



