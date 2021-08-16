import sqlalchemy as sa
from pydantic import validator, BaseModel
from typing import *

from config import BASE


class Position(BASE):
    __tablename__ = 'Position'
    id = sa.Column(sa.Integer, primary_key=True)
    Name = sa.Column(sa.String(50))


class PositionValidation(BaseModel):
    Name: Optional[str] = None

    @validator('Name')
    def position_should_be_str(cls, value):
        if type(value) == str:
            return value
        else:
            raise ValueError('only meaningful text')
