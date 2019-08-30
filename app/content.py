from http import HTTPStatus
from typing import Any, Dict, Type, get_type_hints

from aiohttp import web

from app.resources.base import Resource
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

        result = await call_http_handler(request, handler)
        if isinstance(result, Resource):
            status_code = types_dict.get(result.__class__, HTTPStatus.OK)
            if accept_header and not accept_header == "*/*":
                resource_class = result.media_types().get(accept_header)
                if resource_class:
                    return web.json_response(
                        resource_class.transform_from(result).dict(),
                        status=status_code,
                    )
                else:
                    # Accept Header não suportado
                    return web.json_response(
                        {"error": f"Unsuported media_type: {accept_header}"},
                        status=400,
                    )
            return web.json_response(result.dict(), status=status_code)
        return result

    return _wrap
