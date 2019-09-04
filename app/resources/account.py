import json

from app.resources.base import Resource, MediaType


class Account(Resource):
    id: int
    name: str

    def serialize(self, media_type: MediaType) -> bytes:
        return json.dumps(self.dict()).encode("utf-8")
