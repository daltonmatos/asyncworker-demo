import json

from pydantic import BaseModel

from app.resources.base import (
    Resource,
    MediaType,
    VersionedResource,
    Charset,
    VersionedResourceSpec,
)


class CharsetResource(Resource):
    string: str

    @staticmethod
    def media_types():
        return {
            "application/vnd.charset.v1+json": VersionedResourceSpec(
                charsets=[Charset.UTF16], resource=CharsetResourceV1
            )
        }

    def serialize(self, media_type: MediaType) -> bytes:
        raise NotImplementedError


class CharsetResourceV1(BaseModel, VersionedResource[CharsetResource]):
    other_string: str

    @staticmethod
    def transform_from(base: CharsetResource) -> "CharsetResourceV1":
        return CharsetResourceV1(other_string=base.string)

    def serialize(self, media_type: MediaType) -> bytes:
        return json.dumps(self.dict()).encode(media_type.charset)
