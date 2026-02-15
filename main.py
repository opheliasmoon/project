from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# DATABASE SESSION FUNCTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# USE CASE 1 - VIEW COURSES
# =========================
@app.get("/courses", response_class=HTMLResponse)
def view_courses(request: Request, db: Session = Depends(get_db)):

    courses = db.query(models.Course).all()

    return templates.TemplateResponse("courses.html", {
        "request": request,
        "courses": courses
    })


# =========================
# USE CASE 2 - LOAD ADD PAGE
# =========================
@app.get("/add-course", response_class=HTMLResponse)
def add_course_page(request: Request):
    return templates.TemplateResponse("add_course.html", {
        "request": request
    })


# =========================
# USE CASE 2 - ADD COURSE
# =========================
@app.post("/add-course")
def add_course(
    course_id: str = Form(...),
    course_name: str = Form(...),
    credit_hours: int = Form(...),
    department: str = Form(...),
    db: Session = Depends(get_db)
):

    new_course = models.Course(
        course_id=course_id,
        course_name=course_name,
        credit_hours=credit_hours,
        department=department
    )

    db.add(new_course)
    db.commit()

    return RedirectResponse("/courses", status_code=303)


# =========================
# USE CASE 3 - DELETE COURSE
# =========================
@app.get("/delete-course/{course_id}")
def delete_course(course_id: str, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter(
        models.Course.course_id == course_id
    ).first()

    if course:
        db.delete(course)
        db.commit()

    return RedirectResponse("/courses", status_code=303)


