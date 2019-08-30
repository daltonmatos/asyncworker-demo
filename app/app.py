from functools import partial
from typing import Union

from aiohttp import web

from app.content import content_negotiation
from app.http.status import Status
from app.resources.user import UserResource
from app.types.http import HTTP
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


@app.http(["/users/2"], methods=["GET"])
@content_negotiation
async def users_2() -> HTTP[Status.ACCEPTED, UserResource]:
    return UserResource(id=2, name="Other User", phone="+5511...")
