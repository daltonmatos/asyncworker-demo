from typing import Generic, TypeVar, Union

from app.http.status import HTTPStatus
from app.resources.base import Resource, NotFoundException

Status = TypeVar("Status", bound=HTTPStatus)
_Resource = TypeVar("_Resource", bound=Resource)


class _HTTP(Generic[Status, _Resource]):
    pass


HTTP = Union[_HTTP[Status, _Resource], _Resource]
