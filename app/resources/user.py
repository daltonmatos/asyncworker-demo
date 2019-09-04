import json
import sys
from typing import Dict, Type, Any

from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.resources.base import Resource, VersionedResource, MediaType


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

    def serialize(self, media_type: MediaType) -> bytes:
        pass

    def to_dict(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return self.dict()


if sys.version_info[1] >= 7:

    class UserResourceV1(BaseModel, VersionedResource[UserResource]):
        name: str

        @staticmethod
        def transform_from(base: UserResource) -> "UserResourceV1":
            return UserResourceV1(name=base.name)

        def serialize(self, media_type: MediaType) -> bytes:
            return json.dumps(self.dict()).encode("utf-8")

        def to_dict(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
            return self.dict()

    class UserResourceV2(BaseModel, VersionedResource[UserResource]):
        phone: str

        @staticmethod
        def transform_from(base: UserResource) -> "UserResourceV2":
            return UserResourceV2(phone=base.phone)

        def serialize(self, media_type: MediaType) -> bytes:
            return json.dumps(self.dict()).encode("utf-8")

        def to_dict(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
            return self.dict()


else:

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
