import abc
from typing import Dict, Type

from pydantic import BaseModel


class VersionedResource(BaseModel, abc.ABC):
    @staticmethod
    def transform_from(base: "Resource") -> "VersionedResource":
        raise NotImplementedError


class Resource(BaseModel, abc.ABC):
    @staticmethod
    def media_types() -> Dict[str, Type[VersionedResource]]:
        return {}
