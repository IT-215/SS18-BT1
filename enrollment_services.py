from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Student, Course, Enrollment
from schemas import EnrollmentCreate


# ==== CREATE ENROLLMENT ====
def create_enrollment(db: Session, data: EnrollmentCreate) -> Enrollment:
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if student.status != "ACTIVE":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is not ACTIVE")

    if course.status != "OPEN":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course is not OPEN")

    existed = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already enrolled in this course")

    current_count = db.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if current_count >= course.max_students:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course has reached max_students")

    new_enrollment = Enrollment(student_id=data.student_id, course_id=data.course_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment


# ==== GET STUDENT COURSES ====
def get_student_courses(db: Session, student_id: int) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student
