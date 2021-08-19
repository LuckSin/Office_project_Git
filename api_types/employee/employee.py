import sqlalchemy as sa
from flask import g
import json
import datetime
import os

import models
from config import SESSION
from permissions.base import AccessError


def get_employee_list():
    allowed_employee_ids = g.authority.allowed_objects('employee', 'read').ids
    employees = list(SESSION.execute(sa.select([models.Employee]).where(models.Employee.id.in_(allowed_employee_ids))))
    employees_lists = []
    try:
        g.authority.assert_operation_allowed("employee", "read")
    except AccessError:
        return {'Error': AccessError.message}
    for employee in employees:
        employees_dict = {'id': employee[0].id, 'Department_id': employee[0].Department_id,
                          'Position_id': employee[0].Position_id, 'Salary': employee[0].Salary,
                          'Full_name': employee[0].Full_name, 'Login': employee[0].Login,
                          'Password': employee[0].Password}
        employees_lists.append(employees_dict)
    return employees_lists


def get_employee(id):
    allowed_employee_ids = g.authority.allowed_objects('employee', 'read').ids
    try:
        g.authority.assert_operation_allowed("employee", "read")
    except AccessError:
        return {'Error': AccessError.message}
    employee_tmp = list(SESSION.execute(sa.select([models.Employee])
                                        .where(sa.and_(models.Employee.id == id),
                                               models.Employee.id.in_(allowed_employee_ids))))
    employee_dict = {'id': employee_tmp[0][0].id, 'Department_id': employee_tmp[0][0].Department_id,
                     'Position_id': employee_tmp[0][0].Position_id, 'Salary': employee_tmp[0][0].Salary,
                     'Full_name': employee_tmp[0][0].Full_name, 'Login': employee_tmp[0][0].Login,
                     'Password': employee_tmp[0][0].Password}
    return employee_dict


def insert_employee(data):
    try:
        g.authority.assert_operation_allowed('employee', 'create')
    except AccessError:
        return {'Error': AccessError.message}
    employee = models.EmployeeValidation(**data)
    query = sa.insert(models.Employee).values(
        Department_id=employee.Department_id,
        Position_id=employee.Position_id,
        Salary=employee.Salary,
        Full_name=employee.Full_name,
        Login=employee.Login,
        Password=employee.Password
    )
    result = SESSION.execute(query)
    SESSION.commit()
    return result.inserted_primary_key[0]


def update_employee(data, employee_id):
    allowed_employee_ids = g.authority.allowed_objects('employee', 'update').ids
    employee = models.EmployeeValidation(**data)
    employee_id = int(employee_id)
    validation_data = {
        'Department_id': employee.Department_id,
        'Position_id': employee.Position_id,
        'Salary': employee.Salary,
        'Full_name': employee.Full_name,
        'Login': employee.Login,
        'Password': employee.Password
    }
    try:
        g.authority.assert_operation_allowed('employee', 'update') and employee_id in allowed_employee_ids
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.update(models.Employee).where(models.Employee.id == employee_id).values(**validation_data))
    SESSION.commit()


def delete_employee(id):
    allowed_employee_ids = g.authority.allowed_objects('employee', 'delete').ids
    filters = [models.Employee.id.in_(allowed_employee_ids), ]
    try:
        g.authority.assert_operation_allowed('employee', 'delete')
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.delete(models.Employee).where(sa.and_(*filters, (models.Employee.id == id))))
    SESSION.commit()


def get_employees_salaries_by_department(office_ids, department_ids):
    filters = []
    if office_ids:
        filters.append(models.Office.id.in_(office_ids))
    if department_ids:
        filters.append(models.Department.id.in_(department_ids))
    join_table = list(SESSION.execute(
        sa.select(
            [
                models.Employee,
                models.Department.Name.label('department_name'),
                models.Office.City.label('office_city')
            ]
        ).select_from(
            sa.join(
                models.Employee,
                models.Department,
                models.Employee.Department_id == models.Department.id
            )
            .join(
                models.Office,
                models.Office.id == models.Department.Office_id
            )
        ).where(sa.and_(*filters))
    ))
    salary_lists = []
    finance = 0
    try:
        g.authority.assert_operation_allowed('employee', 'salary')
    except AccessError:
        return {'Error': AccessError.message}
    for salary in join_table:
        salaries_dict = {'Full_name': salary[0].Full_name, 'Salary': salary[0].Salary,
                         'Department_name': salary.department_name, 'Office_city': salary.office_city}
        salary_lists.append(salaries_dict)
        finance += float(salary[0].Salary)
    return salary_lists, finance


def save_json_with_open(data):
    directory = os.getcwd()
    if directory != '/home/pbaiko/PycharmProjects/Office_project_Git_1/json_file':
        os.chdir('json_file')
    with open(f'json_file_type_json_{datetime.date.today()}.json', 'w') as file:
        json.dump(data, file)
