from typing import Dict, Type

from pydantic import BaseModel

from app.resources.base import Resource, VersionedResource


class UserResource(Resource):
    id: int
    name: str
    phone: str

    @staticmethod
    def media_types() -> Dict[str, Type[VersionedResource]]:
        return {
            "application/vnd.app.user.v1+json": UserResourceV1,
            "application/vnd.app.user.v2+json": UserResourceV2,
        }


class UserResourceV1(VersionedResource):
    name: str

    @staticmethod
    def transform_from(base: UserResource) -> "UserResourceV1":
        return UserResourceV1(name=base.name)


class UserResourceV2(VersionedResource):
    phone: str

    @staticmethod
    def transform_from(base: UserResource) -> "UserResourceV2":
        return UserResourceV2(phone=base.phone)
