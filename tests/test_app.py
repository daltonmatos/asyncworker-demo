from http import HTTPStatus

from asynctest import TestCase

from app.app import app
from asyncworker.testing import HttpClientContext


class AppTest(TestCase):
    async def setUp(self):
        self.client_context = HttpClientContext(app)

    async def test_simple_request(self):
        async with self.client_context as client:
            resp = await client.get("/")
            self.assertEqual(200, resp.status)

            resp_data = await resp.json()

            self.assertEqual({}, resp_data)

    async def test_return_simple_resource(self):
        async with self.client_context as client:
            resp = await client.get("/users/1")
            self.assertEqual(200, resp.status)
            resp_data = await resp.json()

            self.assertEqual(
                {"name": "John Doe", "phone": "+5521...", "id": 1}, resp_data
            )

    async def test_request_with_accept_header(self):
        async with self.client_context as client:
            resp = await client.get(
                "/users/1",
                headers={"Accept": "application/vnd.app.user.v1+json"},
            )
            self.assertEqual(200, resp.status)
            resp_data = await resp.json()

            self.assertEqual({"name": "John Doe"}, resp_data)

    async def test_request_with_accept_header_v2(self):
        async with self.client_context as client:
            resp = await client.get(
                "/users/1",
                headers={"Accept": "application/vnd.app.user.v2+json"},
            )
            self.assertEqual(200, resp.status)
            resp_data = await resp.json()

            self.assertEqual({"phone": "+5521..."}, resp_data)

    async def test_request_with_unsuported_media_type(self):
        media_type = "application/vnd.app.user.vunsuported+json"
        async with self.client_context as client:
            resp = await client.get("/users/1", headers={"Accept": media_type})
            self.assertEqual(400, resp.status)
            resp_data = await resp.json()

            self.assertEqual(
                {"error": f"Unsuported media_type: {media_type}"}, resp_data
            )

    async def test_users_2_resource_with_status_code(self):
        async with self.client_context as client:
            resp = await client.get("/users/2")
            self.assertEqual(HTTPStatus.ACCEPTED, resp.status)
            resp_data = await resp.json()

            self.assertEqual(
                {"id": 2, "name": "Other User", "phone": "+5511..."}, resp_data
            )

    async def test_accounts_or_user_resource_with_status_code(self):
        async with self.client_context as client:
            resp = await client.get("/accounts/1")
            self.assertEqual(HTTPStatus.OK, resp.status)
            resp_data = await resp.json()

            self.assertEqual({"id": 1, "name": "Account"}, resp_data)

    async def test_accounts_raise_not_found_exception(self):
        async with self.client_context as client:
            resp = await client.get("/accounts/e")
            self.assertEqual(HTTPStatus.NOT_FOUND, resp.status)
            resp_data = await resp.json()

            self.assertEqual({"error": "Resource not found"}, resp_data)

    async def test_accounts_raise_uncaught_exception(self):
        async with self.client_context as client:
            resp = await client.get("/accounts/u")
            self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, resp.status)

    async def test_resource_specific_charset(self):
        async with self.client_context as client:
            media_type = "application/vnd.charset.v1+json;charset=utf-16"
            value = "✓"
            resp = await client.get(
                "/charsets/1",
                json={"string": value},
                headers={"Accept": media_type},
            )
            self.assertEqual(HTTPStatus.OK, resp.status)
            self.assertEqual(media_type, resp.headers.get("Content-Type"))
            resp_data = await resp.json()
            self.assertEqual(
                value.encode("utf-16"),
                resp_data["other_string"].encode("utf-16"),
            )

    async def test_resource_unsuported_charset(self):
        async with self.client_context as client:
            charset = "utf-32"
            media_type = "application/vnd.charset.v1+json"
            value = "✓"
            resp = await client.get(
                "/charsets/1",
                json={"string": value},
                headers={"Accept": f"{media_type};charset={charset}"},
            )
            self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status)
            resp_data = await resp.json()
            self.assertEqual(
                {
                    "error": f"Unsuported Charset for media_type {media_type}: {charset}"
                },
                resp_data,
            )
