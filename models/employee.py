import sqlalchemy as sa
from sqlalchemy.orm import relationship
from config import BASE
from pydantic import validator, BaseModel
from typing import *


class Employee(BASE):
    __tablename__ = 'Employee'
    id = sa.Column(sa.Integer, primary_key=True)
    Department_id = sa.Column(sa.Integer)
    Department = relationship('Department', foreign_keys=[Department_id],
                              primaryjoin='Department.id==Employee.Department_id')
    Position_id = sa.Column(sa.Integer)
    Position = relationship('Position', foreign_keys=[Position_id], primaryjoin='Position.id==Employee.Position_id')
    Salary = sa.Column(sa.String(50))
    Full_name = sa.Column(sa.String(50))
    Login = sa.Column(sa.String(50))
    Password = sa.Column(sa.String(50))


class EmployeeValidation(BaseModel):
    Department_id: Optional[int] = None
    Position_id: Optional[int] = None
    Salary: Optional[float] = None
    Full_name: Optional[str] = None
    Login: Optional[str] = None
    Password: Optional[str] = None

    @validator('Salary')
    def salary_should_be_float_or_int(cls, v):
        if type(v) == int or type(v) == float:
            return v
        else:
            raise ValueError('Salary can only contain numbers')

    @validator('Password')
    def password_over_eight(cls, v):
        if len(v) >= 8:
            return v
        else:
            raise ValueError('Password must be more than 8 characters')
