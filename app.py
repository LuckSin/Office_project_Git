# !flask/bin/python
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import g

import auth
import config
from models import Employee
from api_types import get_office_list, insert_office, insert_department, insert_employee, insert_position,\
    get_department_list, get_employee_list, get_position_list, update_employee, update_office, update_department,\
    update_position, get_employee, delete_office, delete_department, delete_employee, delete_position, get_office,\
    get_department, get_position, get_employees_salaries_by_department, save_json_with_open
from permissions import Authority

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@127.0.0.1/company_base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


def configure_routes(app):
    @app.before_request
    def setup_context():
        if request.url.replace(f'{request.root_url}', '/') != '/api/v1/login':
            token_header = auth.get_token_auth_header()
            session = config.SESSION
            data = auth.decode_token(token_header, config.jwt_secret_key)
            user = session.query(Employee).filter_by(Login=data['Sub']).first()
            if not user:
                raise auth.AuthenticationError(
                    error_code="invalid-credentials",
                    message="Invalid Credentials!",
                    status_code=401,
                )
            g.user = user
            g.authority = Authority(user)

    @app.route('/api/v1/login', methods=['POST'])
    def get_token_for_login():
        data = request.json
        return auth.views.login_view(data)

    @app.route('/api/v1/offices', methods=['GET'])
    def get_all_offices():
        data = get_office_list()
        return jsonify({'Offices': data})

    @app.route('/api/v1/office/<id>', methods=['GET'])
    def get_office_id(id):
        data = get_office(id)
        return jsonify({'Office': data})

    @app.route('/api/v1/office/create', methods=['POST'])
    def create_office_id():
        data = request.json
        insert_office(data)
        return jsonify({'created office in': data.get('City')},  insert_office(data))

    @app.route('/api/v1/office/<int:id>/update', methods=['PUT'])
    def update_data_office(id):
        data = request.json
        update_office(data, id)
        return jsonify('update office', update_office(data, id))

    @app.route('/api/v1/office/<id>/delete', methods=['DELETE'])
    def delete_data_office(id):
        delete_office(id)
        return jsonify({'delete office': delete_office(id)})

    @app.route('/api/v1/departments', methods=['GET'])
    def get_all_department():
        data = get_department_list()
        return jsonify({'Department': data})

    @app.route('/api/v1/department/<id>', methods=['GET'])
    def get_department_id(id):
        data = get_department(id)
        return jsonify({'Department': data})

    @app.route('/api/v1/department/create', methods=['POST'])
    def create_department():
        data = request.json
        inserted_id = insert_department(data)
        return jsonify('created department', inserted_id)

    @app.route('/api/v1/department/<id>/update', methods=['PUT'])
    def update_data_department(id):
        data = request.json
        update_department(data, id)
        return jsonify(get_department(id))

    @app.route('/api/v1/department/<id>/delete', methods=['DELETE'])
    def delete_data_department(id):
        delete_department(id)
        return jsonify({"message": "department deleted"})

    @app.route('/api/v1/employees', methods=['GET'])
    def get_all_employees():
        data = get_employee_list()
        return jsonify({'Employee': data})

    @app.route('/api/v1/employee/<id>', methods=['GET'])
    def get_employee_id(id):
        data = get_employee(id)
        return jsonify({'Employee': data})

    @app.route('/api/v1/employee/create', methods=['POST'])
    def create_employee():
        data = request.json
        inserted_id = insert_employee(data)
        return jsonify('created employee', inserted_id)

    @app.route('/api/v1/employee/<id>/update', methods=['PUT'])
    def update_data_employee(id):
        data = request.json
        update_employee(data, id)
        return jsonify('update employee', update_employee(data, id))

    @app.route('/api/v1/employee/<id>/delete', methods=['DELETE'])
    def delete_data_employee(id):
        delete_employee(id)
        return jsonify({"message": "employee deleted"})

    @app.route('/api/v1/positions', methods=['GET'])
    def get_all_position():
        data = get_position_list()
        return jsonify({'Position': data})

    @app.route('/api/v1/position/<id>', methods=['GET'])
    def get_position_id(id):
        data = get_position(id)
        return jsonify({'Position': data})

    @app.route('/api/v1/position/create', methods=['POST'])
    def create_position():
        data = request.json
        inserted_id = insert_position(data)
        return jsonify('created position', inserted_id)

    @app.route('/api/v1/position/<id>/update', methods=['PUT'])
    def update_data_position(id):
        data = request.json
        update_position(data, id)
        return jsonify('update position', update_position(data, id))

    @app.route('/api/v1/position/<id>/delete', methods=['DELETE'])
    def delete_data_position(id):
        delete_position(id)
        return jsonify({"message": "position deleted"})

    @app.route('/api/v1/salary', methods=['GET'])
    def get_salary():
        office_ids = request.json.get('office_ids')
        department_ids = request.json.get('department_ids')
        data = get_employees_salaries_by_department(office_ids, department_ids)
        save_json_with_open(data)
        return jsonify({'Salary': data[0], 'Departments costs': data[1]})


if __name__ == '__main__':
    configure_routes(app)
    app.run(debug=config.debug_mode)
