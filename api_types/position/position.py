import sqlalchemy as sa
from config import SESSION
from flask import g

import models


def get_position_list():
    allowed_position_ids = g.authority.allowed_objects('position', 'read').ids
    filters = []
    filters.append(models.Position.id.in_(allowed_position_ids))
    positions = list(SESSION.execute(sa.select([models.Position]).where(sa.and_(*filters))))
    positions_list = []
    if 'read' in g.authority.allowed_operations('position'):
        for position in positions:
            position_dict = {'id': position[0].id, 'Name': position[0].Name}
            positions_list.append(position_dict)
        return positions_list


def get_position(id):
    allowed_position_ids = g.authority.allowed_objects('position', 'read').ids
    filters = [models.Position.id.in_(allowed_position_ids), ]

    if 'read' in g.authority.allowed_operations('position'):
        position = list(SESSION.execute(sa.select([models.Position]).where(models.Position.id == id)))
        position_dict = {'id': position[0][0].id, 'Name': position[0][0].Name}
        return position_dict


def insert_position(data):
    if 'create' in g.authority.allowed_operations('position'):
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

    if 'update' in g.authority.allowed_operations('position') and position_id in allowed_position_ids:
        SESSION.execute(
            sa.update(models.Position).where(models.Position.id == position_id).values(**validation_data))
        SESSION.commit()


def delete_position(id):
    allowed_position_ids = g.authority.allowed_objects('position', 'delete').ids
    filters = [models.Position.id.in_(allowed_position_ids), ]

    if 'delete' in g.authority.allowed_operations('position'):
        SESSION.execute(
            sa.delete(models.Position).where(sa.and_(*filters, (models.Position.id == id))))
        SESSION.commit()
