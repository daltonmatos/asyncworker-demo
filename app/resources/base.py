import abc
from typing import Dict, Type, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class VersionedResource(Generic[T], BaseModel):
    @staticmethod
    def transform_from(base: T) -> "VersionedResource":
        raise NotImplementedError


class Resource(BaseModel, abc.ABC):
    @staticmethod
    def media_types() -> Dict[str, Type[VersionedResource]]:
        return {}
