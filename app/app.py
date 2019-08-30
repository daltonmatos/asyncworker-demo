import json
from functools import partial
from typing import Union

from aiohttp import web

from app.content import content_negotiation
from app.http.status import Status
from app.resources.account import Account
from app.resources.base import NotFoundException
from app.resources.charset import CharsetResource
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


@app.http(["/accounts/{what}"], methods=["GET"])
@content_negotiation
async def accounts(
    request: web.Request
) -> Union[HTTP[Status.OK, Account], NotFoundException]:
    what = request.match_info["what"]
    if what == "e":
        raise NotFoundException(error="Resource not found")

    if what == "u":
        v = 1 / 0

    return Account(id=1, name="Account")


@app.http(["/charsets/1"], methods=["GET"])
@content_negotiation
async def charsets(request: web.Request) -> CharsetResource:
    """
    Precisamos **sempre** setar o media_type e o charset corretos no header
    Content-Type

    Se não fizermos isso o aiohttp, por exemplo, pode colocar `application/octet-stream`
    e isso causa problemas quando fazemos, no client: `await response.json()`.
    Mesmo o conteúdo **sendo** um JSON válido.
    """
    body = await request.json()
    string = body["string"]
    d = {"string": string}
    res = json.dumps(d)

    # return CharsetResource(string=string)
    return web.Response(
        body=res.encode("utf-16"),
        headers={
            "Content-Type": "application/vnd.charset.v1+json;charset=utf-16"
        },
    )
