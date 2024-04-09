#pylint
from fastapi import APIRouter, Body, Request, HTTPException, status
from bson.objectid import ObjectId

from models import Student,StudentId, StudentUpdate

router = APIRouter()

@router.post("/", status_code = status.HTTP_201_CREATED, 
response_model = StudentId , summary = "Create Students", description = '''API to create a student 
            in the system. All fields are mandatory and required while creating
            the student in the system.''',
            response_description='''A JSON 
            response sending back the ID of the newly created student record.
            ''')
async def create_student(request: Request, student: Student = Body(...)):
    student_record = student.model_dump()
    new_student = request.app.database["students"].insert_one(student_record)
    return {"id": str(new_student.inserted_id)}

@router.get("/", status_code = status.HTTP_200_OK, summary = "List students", description='''An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.''', response_description='''sample response''' )
async def list_students(request: Request, country: str | None = None, age: int | None = None):
    students = request.app.database["students"].find()
    result = []
    for student in students:
        if age!=None:
            if student["age"]>=age:
                if country!=None:
                    if student["address"]["country"] == country:
                        result.append({"name":student["name"],
                            "age": student["Age"]})
                else:
                    result.append({"name":student["name"],
                        "age": student["age"]})
            
        elif country!=None:
            if student["country"]==country:
                result.append({"name":student["name"],
                            "age": student["age"]})
        else:
            result.append({"name":student["name"],
                            "age": student["age"]})
   
    return result

@router.get("/{id}", response_model=Student, status_code = status.HTTP_200_OK, summary="Fetch student", description='''An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.''', response_description='''sample response''')
async def get_student(request: Request, id: str): 
    if result := request.app.database["students"].find_one({"_id": ObjectId(id)}):
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {id} not found")

@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Update student", description='''API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.''', response_description='''No content''')
async def update_student(id: str, request: Request,  student: StudentUpdate = Body(...)):
    if  new_values := request.app.database["students"].find_one({"_id": ObjectId(id)}):
        if student.name!=None:
            new_values["name"] = student.name
        if student.age!=None:
            new_values['age'] = student.age
        if student.address!=None:
            if student.address.country!=None:
                new_values["address"]["country"] = student.address.country
            if student.address.city!=None:
                new_values["address"]['city'] = student.address.city
        update_result =  request.app.database["students"].update_one({"_id": ObjectId(id)},  {"$set": new_values})
        if update_result.modified_count==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {id} not found")
 
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {id} not found")


@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Delete student", description='''API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.''', response_description='''sample response''')
async def delete_student(id: str, request: Request):
    delete_result = request.app.database["students"].delete_one({ "_id": ObjectId(id) })
   
    if delete_result.deleted_count == 1:
        return {}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {id} not found")

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_student(request: Request):
    request.app.database["students"].delete_many({})
    return {}
