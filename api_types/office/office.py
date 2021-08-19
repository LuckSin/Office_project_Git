import sqlalchemy as sa
from config import SESSION
from flask import g

from permissions.base import AccessError
import models


def get_office_list():
    allowed_office_ids = g.authority.allowed_objects('office', 'read').ids
    offices = list(SESSION.execute(sa.select([models.Office]).where(models.Office.id.in_(allowed_office_ids))))
    offices_lists = []
    try:
        g.authority.assert_operation_allowed("office", "read")
    except AccessError:
        return {'Error': AccessError.message}
    for office in offices:
        office_dict = {'id': office[0].id, 'City': office[0].City}
        offices_lists.append(office_dict)
    return offices_lists


def get_office(id):
    allowed_office_ids = g.authority.allowed_objects('office', 'read').ids
    try:
        g.authority.assert_operation_allowed("office", "read")
    except AccessError:
        return {'Error': AccessError.message}
    office = list(SESSION.execute(sa.select([models.Office]).where(sa.and_(models.Office.id == id),
                                                                   models.Office.id.in_(allowed_office_ids))))
    office_dict = {'id': office[0][0].id, 'City': office[0][0].City}
    return office_dict


def insert_office(data):
    try:
        g.authority.assert_operation_allowed('office', 'create')
    except AccessError:
        return {'Error': AccessError.message}
    office = models.OfficeValidation(**data)
    query = sa.insert(models.Office).values(
        City=office.City
    )
    result = SESSION.execute(query)
    SESSION.commit()
    return result.inserted_primary_key[0]


def update_office(data, city_id):
    allowed_office_ids = g.authority.allowed_objects('office', 'update').ids
    office = models.OfficeValidation(**data)
    city_id = int(city_id)
    validation_data = {
        'City': office.City
    }
    try:
        g.authority.assert_operation_allowed('office', 'update') and city_id in allowed_office_ids
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.update(models.Office).where(models.Office.id == city_id).values(**validation_data))
    SESSION.commit()


def delete_office(id):
    allowed_office_ids = g.authority.allowed_objects('office', 'delete').ids
    filters = [models.Office.id.in_(allowed_office_ids), ]

    try:
        g.authority.assert_operation_allowed('office', 'delete')
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.delete(models.Office).where(sa.and_(*filters, (models.Office.id == id))))
    SESSION.commit()
