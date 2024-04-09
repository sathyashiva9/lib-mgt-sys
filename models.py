from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class StudentId(BaseModel):
    id: str

class Student(BaseModel):
    name: str 
    age: int
    address: Address

class AddressUpdate(BaseModel):
    city: str | None = None
    country: str | None =None

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None 
    address: AddressUpdate | None = None