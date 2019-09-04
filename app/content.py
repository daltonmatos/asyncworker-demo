from http import HTTPStatus
from typing import get_type_hints

from aiohttp import web

from app.resources.base import HTTPException, Resource, MediaType
from app.types.http import _HTTP
from asyncworker.routes import call_http_handler


def build_return_type_dict(return_type):
    result = {}
    args = getattr(return_type, "__args__", None)
    while args:
        for arg in args:
            if hasattr(arg, "__args__") and arg.__origin__ is _HTTP:
                result[arg.__args__[1]] = arg.__args__[0].status
            args = getattr(arg, "__args__", None)
    return result


def content_negotiation(handler):
    async def _wrap(request: web.Request):
        accept_header = request.headers.get("Accept")
        return_type = get_type_hints(handler).get("return")
        if return_type:
            types_dict = build_return_type_dict(return_type)

        try:
            result = await call_http_handler(request, handler)
        except HTTPException as http_exc:
            return web.json_response(http_exc.dict(), status=http_exc.status)

        if isinstance(result, Resource):
            status_code = types_dict.get(result.__class__, HTTPStatus.OK)
            if accept_header and not accept_header == "*/*":
                media_type = accept_header.split(";")[0]
                resource_spec = result.media_types().get(media_type)
                if resource_spec:
                    charset = accept_header.split("=")[1]
                    if charset not in resource_spec.charsets:
                        return web.json_response(
                            {
                                "error": f"Unsuported Charset for media_type {media_type}: {charset}"
                            },
                            status=HTTPStatus.BAD_REQUEST,
                        )
                    return web.Response(
                        body=resource_spec.resource.transform_from(
                            result
                        ).serialize(MediaType.parse(accept_header)),
                        status=status_code,
                        headers={"Content-Type": accept_header},
                    )
                else:
                    # Accept Header não suportado
                    return web.json_response(
                        {"error": f"Unsuported media_type: {accept_header}"},
                        status=HTTPStatus.BAD_REQUEST,
                    )
            return web.json_response(result.dict(), status=status_code)
        return result

    return _wrap
