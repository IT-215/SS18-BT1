from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import EnrollmentCreate, EnrollmentResponse, StudentCoursesResponse, CourseOut
import enrollment_services as services

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Registration API")


# ==== POST /enrollments ====
@app.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def register_course(data: EnrollmentCreate, db: Session = Depends(get_db)):
    return services.create_enrollment(db, data)


# ==== GET /students/{student_id}/courses ====
@app.get("/students/{student_id}/courses", response_model=StudentCoursesResponse)
def get_courses_of_student(student_id: int, db: Session = Depends(get_db)):
    student = services.get_student_courses(db, student_id)
    courses = [enrollment.course for enrollment in student.enrollments]
    return StudentCoursesResponse(
        student_id=student.id,
        full_name=student.full_name,
        courses=[CourseOut.model_validate(c) for c in courses]
    )
