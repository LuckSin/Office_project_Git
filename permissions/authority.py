from typing import *

from models import Employee
from .base import AllowedSet, PermissionAuthority
from .resources.meta import get_authority_class_by_resource


class Authority(PermissionAuthority):
    def __init__(self, employee: Employee):
        self.employee = employee

    def get_authority_for(self, resource_type: str):
        authority_class = get_authority_class_by_resource(resource_type)
        authority = authority_class(self.employee)
        return authority

    def allowed_objects(self, resource_type: str, operation: str) -> AllowedSet:
        authority = self.get_authority_for(resource_type)
        return authority.allowed_objects(resource_type, operation)

    def allowed_operations(self, resource_type: str) -> FrozenSet[str]:
        authority = self.get_authority_for(resource_type)
        return authority.allowed_operations(resource_type)
