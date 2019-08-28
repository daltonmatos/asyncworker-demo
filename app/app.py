from functools import partialmethod, partial

from aiohttp import web

from app.content import content_negotiation
from app.resources.base import Resource
from app.resources.user import UserResource
from asyncworker import App, RouteTypes

app = App()


app.http = partial(app.route, type=RouteTypes.HTTP)


@app.http(["/"], methods=["GET"])
@content_negotiation
async def handler():
    return web.json_response({})


@app.http(["/users/1"], methods=["GET"])
@content_negotiation
async def users() -> UserResource:
    return UserResource(id=1, name="John Doe", phone="+5521...")
