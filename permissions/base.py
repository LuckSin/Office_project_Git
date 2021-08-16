import abc
from dataclasses import dataclass
from typing import *


class AccessError(Exception):
    def __init__(
            self,
            massage: str = 'access denied'
    ):
        super().__init__(massage)


@dataclass
class AllowedSet:
    ids: FrozenSet[Any]

    @classmethod
    def empty(cls):
        return AllowedSet(ids=frozenset())


class PermissionAuthority(abc.ABC):

    @abc.abstractmethod
    def allowed_objects(self, resource_type: str, operation: str) -> AllowedSet:
        raise NotImplementedError()

    def assert_object_allowed(self, resource_type: str, operation: str, instance_id: Any):
        if instance_id not in self.allowed_objects(resource_type, operation).ids:
            raise AccessError()

    @abc.abstractmethod
    def allowed_operations(self, resource_type: str) -> FrozenSet[str]:
        raise NotImplementedError()

    def assert_operation_allowed(self, resource_type: str, operation: str):
        if operation not in self.allowed_operations(resource_type):
            raise AccessError()
