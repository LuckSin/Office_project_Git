import sqlalchemy as sa
from sqlalchemy.orm import relationship
from pydantic import validator, BaseModel

from config import BASE


class Department(BASE):
    __tablename__ = 'Department'
    id = sa.Column(sa.Integer, primary_key=True)
    Office_id = sa.Column(sa.Integer)
    Office = relationship('Office', foreign_keys=[Office_id], primaryjoin='Department.Office_id==Office.id')
    Name = sa.Column(sa.String(50))


class DepartmentValidation(BaseModel):
    Office_id: int
    Name: str

    @validator('Office_id')
    def office_id_should_be_float_or_int(cls, value):
        if type(value) == int or type(value) == float:
            return value
        else:
            raise ValueError('Office_id can only contain numbers')
