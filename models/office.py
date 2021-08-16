import sqlalchemy as sa
from pydantic import validator, BaseModel

from config import BASE


class Office(BASE):
    __tablename__ = 'Office'
    id = sa.Column(sa.Integer, primary_key=True)
    City = sa.Column(sa.String(50))


class OfficeValidation(BaseModel):
    City: str

    @validator('City')
    def city_should_be_str(cls, value):
        if type(value) == str:
            return value
        else:
            raise ValueError('only meaningful text')
