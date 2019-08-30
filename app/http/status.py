from http import HTTPStatus as _HTTPStatus


class HTTPStatus:
    status: int = -1


class Status:
    class OK(HTTPStatus):
        status = _HTTPStatus.OK

    class NOT_FOUND(HTTPStatus):
        status = _HTTPStatus.NOT_FOUND

    class ACCEPTED(HTTPStatus):
        status = _HTTPStatus.ACCEPTED
