import sys
from http import HTTPStatus
from typing import Dict, Type, Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

if sys.version_info[1] >= 7:

    class VersionedResource(GenericModel, Generic[T]):
        @staticmethod
        def transform_from(base: T) -> "VersionedResource":
            raise NotImplementedError


else:

    class VersionedResource(BaseModel):
        @staticmethod
        def transform_from(base) -> "VersionedResource":
            raise NotImplementedError


class Resource(BaseModel):
    @staticmethod
    def media_types() -> Dict[str, Type[VersionedResource]]:
        return {}


class HTTPException(Exception):
    status = -1

    error: str

    def __init__(self, error: str) -> None:
        self.error = error

    def dict(self):
        return {"error": self.error}


class NotFoundException(HTTPException):
    status = HTTPStatus.NOT_FOUND
