from typing import FrozenSet

import sqlalchemy as sa
import config
import models as mod
from ..base import AllowedSet
from .meta import register_authority_class, ResourceAuthority


@register_authority_class
class EmployeeAuthority(ResourceAuthority):
    RESOURCE_TYPE = 'employee'
    fields = [
        'Department_id',
        'Position_id',
        'Salary',
        'Full_name',
        'Login',
        'Password'
    ]

    def allowed_operations(self, resource_type: str) -> FrozenSet[str]:
        self.check_resource(resource_type)
        operations = set()

        if self.employee.Position_id == 1:
            operations.add('read')
            operations.add('update')
            operations.add('delete')
            operations.add('create')
            operations.add('salary')
        if self.employee.Position_id == 3:
            operations.add('read')
            operations.add('update')
            operations.add('delete')
            operations.add('create')
            operations.add('salary')
        if self.employee.Position_id == 4:
            operations.add('read')
            operations.add('update')
            operations.add('delete')
            operations.add('create')
        if self.employee.Position_id == 5:
            operations.add('read')
        return frozenset(operations)


    def ownership_filter(self):
        filters = []
        if self.employee.Position_id == 5:
            filters.append(mod.Employee.id == self.employee.id)

        allowed_ids = {
            employee_id
            for (employee_id, )
            in config.SESSION.execute(sa.select([mod.Employee.id]).where(sa.and_(*filters)))
        }

        return allowed_ids

    def allowed_objects_for_read(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))

    def allowed_objects_for_update(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))

    def allowed_objects_for_delete(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))

    def allowed_objects_for_create(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))

    def allowed_objects_for_salary(self) -> AllowedSet:
        return AllowedSet(ids=frozenset(self.ownership_filter()))
