import sqlalchemy as sa
from config import SESSION
from flask import g

import models
from permissions.base import AccessError

def get_position_list():
    allowed_position_ids = g.authority.allowed_objects('position', 'read').ids
    filters = [models.Position.id.in_(allowed_position_ids), ]
    positions = list(SESSION.execute(sa.select([models.Position]).where(sa.and_(*filters))))
    positions_list = []
    try:
        g.authority.assert_operation_allowed("position", "read")
    except AccessError:
        return {'Error': AccessError.message}
    for position in positions:
        position_dict = {'id': position[0].id, 'Name': position[0].Name}
        positions_list.append(position_dict)
    return positions_list


def get_position(id):
    allowed_position_ids = g.authority.allowed_objects('position', 'read').ids
    try:
        g.authority.assert_operation_allowed("position", "read")
    except AccessError:
        return {'Error': AccessError.message}
    position = list(SESSION.execute(sa.select([models.Position]).
                                    where(sa.and_(models.Position.id == id),
                                          models.Position.id.in_(allowed_position_ids))))
    position_dict = {'id': position[0][0].id, 'Name': position[0][0].Name}
    return position_dict


def insert_position(data):
    try:
        g.authority.assert_operation_allowed('position', 'create')
    except AccessError:
        return {'Error': AccessError.message}
    position = models.PositionValidation(**data)
    query = sa.insert(models.Position).values(
        Name=position.Name
    )
    result = SESSION.execute(query)
    SESSION.commit()
    return result.inserted_primary_key[0]


def update_position(data, position_id):
    allowed_position_ids = g.authority.allowed_objects('position', 'update').ids
    position = models.PositionValidation(**data)
    position_id = int(position_id)
    validation_data = {
        "Name": position.Name
    }
    try:
        g.authority.assert_operation_allowed('position', 'update') and position_id in allowed_position_ids
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.update(models.Position).where(models.Position.id == position_id).values(**validation_data))
    SESSION.commit()


def delete_position(id):
    allowed_position_ids = g.authority.allowed_objects('position', 'delete').ids
    filters = [models.Position.id.in_(allowed_position_ids), ]
    try:
        g.authority.assert_operation_allowed('position', 'delete')
    except AccessError:
        return {'Error': AccessError.message}
    SESSION.execute(
        sa.delete(models.Position).where(sa.and_(*filters, (models.Position.id == id))))
    SESSION.commit()
