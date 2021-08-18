from typing import FrozenSet

import sqlalchemy as sa
import config
from config import POSITIONS
import models as mod
from ..base import AllowedSet
from .meta import register_authority_class, ResourceAuthority


@register_authority_class
class DepartmentAuthority(ResourceAuthority):
    RESOURCE_TYPE = 'department'
    fields = [
        'Office_id',
        'Name'
    ]

    def allowed_operations(self, resource_type: str) -> FrozenSet[str]:
        self.check_resource(resource_type)
        operations = set()

        if self.employee.Position_id == POSITIONS['admin']:
            operations.add('read')
            operations.add('update')
            operations.add('delete')
            operations.add('create')
        if self.employee.Position_id == POSITIONS['head_of_company']:
            operations.add('read')
            operations.add('update')
            operations.add('delete')
            operations.add('create')

        if self.employee.Position_id == POSITIONS['head_of_department']:
            operations.add('read')
            operations.add('update')
            operations.add('delete')
            operations.add('create')
        return frozenset(operations)


    def ownership_filter(self):
        allowed_ids = {
            department_id
            for (department_id, )
            in config.SESSION.execute(sa.select([mod.Department.id]))
        }

        return allowed_ids

    def allowed_objects_for_read(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))

    def allowed_objects_for_update(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))

    def allowed_objects_for_delete(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))
