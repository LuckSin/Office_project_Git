import abc
from typing import *

from models import Employee, Position, Department, Office
from ..base import AllowedSet, PermissionAuthority


AUTHORITY_BY_RESOURCE = {}


def register_authority_class(cls):
    AUTHORITY_BY_RESOURCE[cls.RESOURCE_TYPE] = cls
    return cls


def get_authority_class_by_resource(resource_type: str):
    return AUTHORITY_BY_RESOURCE[resource_type]


class ResourceAuthority(PermissionAuthority, abc.ABC):
    RESOURCE_TYPE: Optional[str] = None

    def __init__(self, employee: Employee):
        self.employee = employee

    def check_resource(self, resource_type: str):
        if resource_type != self.RESOURCE_TYPE:
            raise RuntimeError(f"can't answer permission on {resource_type}")

    def allowed_objects(self, resource_type: str, operation: str) -> AllowedSet:
        self.check_resource(resource_type)
        if operation not in self.allowed_operations(resource_type):
            return AllowedSet.empty()

        method_name = f'allowed_objects_for_{operation}'
        return getattr(self, method_name)()
