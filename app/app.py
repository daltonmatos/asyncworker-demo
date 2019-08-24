import abc
from typing import Dict, Union, Type

from aiohttp import web
from pydantic import BaseModel

from asyncworker import App, RouteTypes

app = App()


def content_negotiation(handler):
    async def _wrap(request: web.Request):
        accept_header = request.headers.get("Accept")

        result = await handler()
        if isinstance(result, Resource):
            if accept_header and not accept_header == "*/*":
                resource_class = result.media_types().get(accept_header)
                if resource_class:
                    return web.json_response(
                        resource_class.transform_from(result).dict()
                    )
                else:
                    # Accept Header não suportado
                    return web.json_response(
                        {"error": f"Unsuported media_type: {accept_header}"},
                        status=400,
                    )
            return web.json_response(result.dict())
        return result

    return _wrap


class VersionedResource(BaseModel, abc.ABC):
    @staticmethod
    def transform_from(base: "Resource") -> "VersionedResource":
        raise NotImplementedError


class Resource(BaseModel, abc.ABC):
    @staticmethod
    def media_types() -> Dict[str, Type[VersionedResource]]:
        return {}


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


@app.route(["/"], type=RouteTypes.HTTP, methods=["GET"])
@content_negotiation
async def handler():
    return web.json_response({})


@app.route(["/users/1"], type=RouteTypes.HTTP, methods=["GET"])
@content_negotiation
async def users() -> UserResource:
    return UserResource(id=1, name="John Doe", phone="+5521...")
