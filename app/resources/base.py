import abc
import sys
from enum import Enum
from http import HTTPStatus
from typing import Dict, Type, Generic, Optional, List

from pydantic import BaseModel


class Charset(str, Enum):
    UTF8 = "utf-8"
    UTF16 = "utf-16"
    UTF32 = "utf-32"
    USASCII = "us-ascii"
    LATIN1 = "latin-1"


class MediaType(BaseModel):
    type: str = "application"
    facet: Optional[str]
    subtype: str = "json"
    charset: Charset = Charset.UTF8
    format: str = "json"

    @staticmethod
    def parse(media_type: str) -> "MediaType":
        type = media_type.split("/")[0]
        subtype = media_type.split("/")[1].split("+")[0]
        charset = Charset.UTF16 if "utf-16" in media_type else Charset.UTF8
        return MediaType(subtype=subtype, charset=charset, type=type)


class SerializableResource(abc.ABC):
    @abc.abstractmethod
    def serialize(self, media_type: MediaType) -> bytes:
        raise NotImplementedError


if sys.version_info[1] >= 7:

    class VersionedResource(Generic[T], SerializableResource):
        @staticmethod
        def transform_from(base: T) -> "VersionedResource":
            raise NotImplementedError


else:

    class VersionedResource(BaseModel):
        @staticmethod
        def transform_from(base) -> "VersionedResource":
            raise NotImplementedError


class Resource(BaseModel, SerializableResource):
    @staticmethod
    def media_types() -> Dict[str, Type[VersionedResource]]:
        return {}


class VersionedResourceSpec:
    charsets: List[Charset]
    resource: VersionedResource

    def __init__(self, charsets, resource) -> None:
        self.charsets = charsets
        self.resource = resource


class HTTPException(Exception):
    status = -1

    error: str

    def __init__(self, error: str) -> None:
        self.error = error

    def dict(self):
        return {"error": self.error}


class NotFoundException(HTTPException):
    status = HTTPStatus.NOT_FOUND
