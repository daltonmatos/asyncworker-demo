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
