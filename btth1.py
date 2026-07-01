from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class CreateCourse(BaseModel):
    code: str
    name: str = Field(min_length=1)
    duration: int = Field(gt=0)
    fee: int = Field(ge=0)

@app.post('/courses')
def create_course(new_course: CreateCourse):
    courses.append({'id': max([c.get('id') for c in courses], default=0) + 1, **new_course.dict()})
    raise HTTPException (
        status_code=201,
        detail='Thêm khóa học thành công'
    )
    
@app.get('/courses/{course_id}')
def find_course_by_id(course_id: int):
    return next((c for c in courses if c.get('id') == course_id), None)

@app.put('/courses/{course_id}')
def update_course(course_id: int, update_course: CreateCourse):
    for course in courses:
        if course.get('id') == course_id:
            course.update(update_course.dict())
            return {
                'message': 'Cập nhật thành công'
            }
            
    return {
        'message': 'Không tìm thấy khóa học'
    }

@app.delete('/courses/{course_id}')
def delete_course(course_id: int):
    for course in courses:
        if course.get('id') == course_id:
            courses.remove(course)
            return {
                'message': 'Xóa thành công'
            }
    return {
        'message': 'Không tìm thấy khóa học'
    }
    
@app.get("/courses")
def get_courses(
    keyword: Optional[str] = None,
    min_fee: Optional[float] = None,
    max_fee: Optional[float] = None
):
    filtered_courses = courses

    if keyword:
        keyword_lower = keyword.lower()
        filtered_courses = [
            course for course in filtered_courses 
            if keyword_lower in course["name"].lower() or keyword_lower in course["code"].lower()
        ]

    if min_fee:
        filtered_courses = [course for course in filtered_courses if course["fee"] >= min_fee]

    if max_fee:
        filtered_courses = [course for course in filtered_courses if course["fee"] <= max_fee]

    return filtered_courses