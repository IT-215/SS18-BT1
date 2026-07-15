from pydantic import BaseModel
from datetime import datetime
from typing import List

# ==== ENROLLMENT ====
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime

    class Config:
        from_attributes = True


# ==== COURSE ====
class CourseOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# ==== STUDENT COURSES ====
class StudentCoursesResponse(BaseModel):
    student_id: int
    full_name: str
    courses: List[CourseOut]
