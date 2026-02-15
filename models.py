from sqlalchemy import Column, String, Integer
from database import Base

class Course(Base):
    __tablename__ = "Courses"

    course_id = Column(String(10), primary_key=True)
    course_name = Column(String(50))
    credit_hours = Column(Integer)
    department = Column(String(50))

