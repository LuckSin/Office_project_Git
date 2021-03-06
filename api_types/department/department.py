import sqlalchemy as sa
from config import SESSION
from flask import g

from permissions.base import AccessError
import models


def get_department_list():
    allowed_department_ids = g.authority.allowed_objects('department', 'read').ids
    filters = []
    filters.append(models.Department.id.in_(allowed_department_ids))
    departments = list(SESSION.execute(sa.select([models.Department]).where(sa.and_(*filters))))
    departments_lists = []
    try:
        g.authority.assert_operation_allowed("department", "read")
    except AccessError:
        return {'Error': AccessError.message}
    for department in departments:
        department_dict = {'id': department[0].id, 'Office_id': department[0].Office_id, 'Name': department[0].Name}
        departments_lists.append(department_dict)
    return departments_lists


def get_department(id):
    allowed_department_ids = g.authority.allowed_objects('department', 'read').ids
    try:
        g.authority.assert_operation_allowed("department", "read")
    except AccessError:
        return {'Error': AccessError.message}
    department = list(SESSION.execute(sa.select([models.Department]).where(sa.and_(models.Department.id == id),
                                                                           models.Department.id.in_
                                                                           (allowed_department_ids))))
    department_dict = {'Office_id': department[0][0].Office_id, 'Name': department[0][0].Name}
    return department_dict


def insert_department(data):
    try:
        g.authority.assert_operation_allowed('department', 'create')
    except AccessError:
        return {'Error': AccessError.message}
    department = models.DepartmentValidation(**data)
    query = sa.insert(models.Department).values(
        Office_id=department.Office_id,
        Name=department.Name
    )
    result = SESSION.execute(query)
    SESSION.commit()
    return result.inserted_primary_key[0]


def update_department(data, department_id):
    allowed_department_ids = g.authority.allowed_objects('department', 'update').ids
    department = models.DepartmentValidation(**data)
    department_id = int(department_id)
    validation_data = {
        'Office_id': department.Office_id,
        'Name': department.Name
    }
    try:
        g.authority.assert_operation_allowed('department', 'update') and department_id in allowed_department_ids
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.update(models.Department).where(models.Department.id == department_id).values(**validation_data))
    SESSION.commit()


def delete_department(id):
    allowed_department_ids = g.authority.allowed_objects('department', 'delete').ids
    filters = [models.Department.id.in_(allowed_department_ids), ]
    try:
        g.authority.assert_operation_allowed('department', 'delete')
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.delete(models.Department).where(sa.and_(*filters, (models.Department.id == id))))
    SESSION.commit()
