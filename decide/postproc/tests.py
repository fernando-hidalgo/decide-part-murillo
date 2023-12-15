from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods

common_options = [
    {"option": "Amarillo", "number": 1, "votes": 47000},
    {"option": "Blanco", "number": 2, "votes": 16000},
    {"option": "Rojo", "number": 3, "votes": 15900},
    {"option": "Verde", "number": 4, "votes": 12000},
    {"option": "Azul", "number": 5, "votes": 6000},
    {"option": "Rosa", "number": 6, "votes": 3100},
]


class PostProcTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def test_identity(self):
        data = {
            "type": "IDENTITY",
            "options": [
                {"option": "Option 1", "number": 1, "votes": 5},
                {"option": "Option 2", "number": 2, "votes": 0},
                {"option": "Option 3", "number": 3, "votes": 3},
                {"option": "Option 4", "number": 4, "votes": 2},
                {"option": "Option 5", "number": 5, "votes": 5},
                {"option": "Option 6", "number": 6, "votes": 1},
            ],
        }

        expected_result = [
            {"option": "Option 1", "number": 1, "votes": 5, "postproc": 5},
            {"option": "Option 5", "number": 5, "votes": 5, "postproc": 5},
            {"option": "Option 3", "number": 3, "votes": 3, "postproc": 3},
            {"option": "Option 4", "number": 4, "votes": 2, "postproc": 2},
            {"option": "Option 6", "number": 6, "votes": 1, "postproc": 1},
            {"option": "Option 2", "number": 2, "votes": 0, "postproc": 0},
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_dhont_1(self):
        data = {
            "type": "HONT",
            "options": common_options,
        }
        expected_result = [
            {"option": "Amarillo", "number": 1, "votes": 47000, "seats": 5},
            {"option": "Blanco", "number": 2, "votes": 16000, "seats": 2},
            {"option": "Rojo", "number": 3, "votes": 15900, "seats": 2},
            {"option": "Verde", "number": 4, "votes": 12000, "seats": 1},
            {"option": "Azul", "number": 5, "votes": 6000, "seats": 0},
            {"option": "Rosa", "number": 6, "votes": 3100, "seats": 0},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_sainte_lague_1(self):
        data = {
            "type": "LAGUE",
            "options": common_options,
        }
        expected_result = [
            {"option": "Amarillo", "number": 1, "votes": 47000, "seats": 3},
            {"option": "Blanco", "number": 2, "votes": 16000, "seats": 2},
            {"option": "Rojo", "number": 3, "votes": 15900, "seats": 2},
            {"option": "Verde", "number": 4, "votes": 12000, "seats": 2},
            {"option": "Azul", "number": 5, "votes": 6000, "seats": 1},
            {"option": "Rosa", "number": 6, "votes": 3100, "seats": 0},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_dhont_2(self):
        data = {
            "type": "HONT",
            "options": [
                {"option": "Party A", "number": 1, "votes": 60000},
                {"option": "Party B", "number": 2, "votes": 40000},
                {"option": "Party C", "number": 3, "votes": 25000},
            ],
        }
        expected_result = [
            {"option": "Party A", "number": 1, "votes": 60000, "seats": 5},
            {"option": "Party B", "number": 2, "votes": 40000, "seats": 3},
            {"option": "Party C", "number": 3, "votes": 25000, "seats": 2},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_sainte_lague_2(self):
        data = {
            "type": "LAGUE",
            "options": [
                {"option": "Party X", "number": 1, "votes": 80000},
                {"option": "Party Y", "number": 2, "votes": 30000},
                {"option": "Party Z", "number": 3, "votes": 20000},
            ],
        }
        expected_result = [
            {"option": "Party X", "number": 1, "votes": 80000, "seats": 4},
            {"option": "Party Y", "number": 2, "votes": 30000, "seats": 3},
            {"option": "Party Z", "number": 3, "votes": 20000, "seats": 3},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_dhont_3(self):
        data = {
            "type": "HONT",
            "options": [
                {"option": "Party P", "number": 1, "votes": 35000},
                {"option": "Party Q", "number": 2, "votes": 28000},
                {"option": "Party R", "number": 3, "votes": 18000},
                {"option": "Party S", "number": 4, "votes": 12000},
            ],
        }
        expected_result = [
            {"option": "Party P", "number": 1, "votes": 35000, "seats": 4},
            {"option": "Party Q", "number": 2, "votes": 28000, "seats": 3},
            {"option": "Party R", "number": 3, "votes": 18000, "seats": 2},
            {"option": "Party S", "number": 4, "votes": 12000, "seats": 1},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_sainte_lague_3(self):
        data = {
            "type": "LAGUE",
            "options": [
                {"option": "Party M", "number": 1, "votes": 42000},
                {"option": "Party N", "number": 2, "votes": 32000},
                {"option": "Party O", "number": 3, "votes": 25000},
                {"option": "Party T", "number": 4, "votes": 18000},
            ],
        }
        expected_result = [
            {"option": "Party M", "number": 1, "votes": 42000, "seats": 3},
            {"option": "Party N", "number": 2, "votes": 32000, "seats": 3},
            {"option": "Party O", "number": 3, "votes": 25000, "seats": 2},
            {"option": "Party T", "number": 4, "votes": 18000, "seats": 2},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_dhont_4(self):
        data = {
            "type": "HONT",
            "options": [
                {"option": "Party P", "number": 1, "votes": 35000},
                {"option": "Party Q", "number": 2, "votes": 28000},
                {"option": "Party R", "number": 3, "votes": 18000},
                {"option": "Party S", "number": 4, "votes": 12000},
            ],
            "preference": True,
        }
        expected_result = [
            {"option": "Party P", "number": 1, "votes": 35000, "seats": 1},
            {"option": "Party Q", "number": 2, "votes": 28000, "seats": 2},
            {"option": "Party R", "number": 3, "votes": 18000, "seats": 3},
            {"option": "Party S", "number": 4, "votes": 12000, "seats": 4},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_sainte_lague_4(self):
        data = {
            "type": "LAGUE",
            "options": [
                {"option": "Party M", "number": 1, "votes": 42000},
                {"option": "Party N", "number": 2, "votes": 32000},
                {"option": "Party O", "number": 3, "votes": 25000},
                {"option": "Party T", "number": 4, "votes": 18000},
            ],
            "preference": True,
        }
        expected_result = [
            {"option": "Party M", "number": 1, "votes": 42000, "seats": 2},
            {"option": "Party N", "number": 2, "votes": 32000, "seats": 2},
            {"option": "Party O", "number": 3, "votes": 25000, "seats": 3},
            {"option": "Party T", "number": 4, "votes": 18000, "seats": 3},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )
