import sqlalchemy as sa
from config import SESSION
from flask import g
from permissions.base import AccessError

import models


def get_office_list():
    allowed_office_ids = g.authority.allowed_objects('office', 'read').ids
    filters = [models.Office.id.in_(allowed_office_ids), ]
    offices = list(SESSION.execute(sa.select([models.Office]).where(sa.and_(*filters))))
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

    if 'read' in g.authority.allowed_operations('office'):
        office = list(SESSION.execute(sa.select([models.Office]).where(sa.and_(models.Office.id == id),
                                                                       models.Office.id.in_(allowed_office_ids))))
        office_dict = {'id': office[0][0].id, 'City': office[0][0].City}
        return office_dict


def insert_office(data):
    if 'create' in g.authority.allowed_operations('office'):
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
    if 'update' in g.authority.allowed_operations('office') and city_id in allowed_office_ids:
        SESSION.execute(
            sa.update(models.Office).where(models.Office.id == city_id).values(**validation_data))
        SESSION.commit()


def delete_office(id):
    allowed_office_ids = g.authority.allowed_objects('office', 'update').ids
    filters = [models.Office.id.in_(allowed_office_ids), ]

    if 'update' in g.authority.allowed_operations('office'):
        SESSION.execute(
            sa.delete(models.Office).where(sa.and_(*filters, (models.Office.id == id))))
        SESSION.commit()
