from fastapi import FastAPI, HTTPException, status
from typing import Union, Optional
from pydantic import BaseModel

app = FastAPI()

class Course(BaseModel):
    title: str
    teacher: str
    students: Optional[list[str]] = []
    level: str

courses = {
    1: {
        "title": "Modern History",
        "teacher": "Ms. Doe",
        "students": ["Harry Potter", "Frodo Baggins"],
        "level": "advanced"
    },
    2: {
        "title": "Mathematics",
        "teacher": "Mr. Davies",
        "students": ["John Smith", "Bruce Lee"],
        "level": "beginner"
    },
    3: {
        "title": "Geography",
        "teacher": "Ms. Apple",
        "students": ["Michael Jordan", "Bruce Lee"],
        "level": "advanced"
    }
}

@app.get("/api/hello/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/api/courses/")
def get_courses(level: Union[str, None] = None):
    if level:
        level_course = []
        for index in courses.keys():
            if courses[index]["level"] == level:
                level_course.append(courses[index])
        return level_course
    return courses

@app.get("/api/courses/{course_id}/")
def get_course(course_id: int):
    try:
        return courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Course with id: {course_id} was not found!"
        )
        
@app.delete("/api/courses/{course_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    try:
        del courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Course with id: {course_id} was not found!"
        )

@app.post("/api/courses/", status_code=status.HTTP_201_CREATED)
def create_course(new_course: Course):
    course_id = max(courses.keys()) + 1
    courses[course_id] = new_course.dict()
    return courses[course_id]

@app.put("/api/courses/{course_id}/")
def update_course(course_id: int, updated_course: Course):
    try:
        course = courses[course_id]
        course["title"] = updated_course.title
        course["teacher"] = updated_course.teacher
        course["students"] = updated_course.students
        course["level"] = updated_course.level
        return course
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Course with id: {course_id} was not found!"
        )