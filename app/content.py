from aiohttp import web

from app.resources.base import Resource


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
