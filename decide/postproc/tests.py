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


    def test_dhont(self):
        data = {
            "type": "HONT",
            "options": common_options,
        }
        expected_result = [
                {"option": "Amarillo", "number": 1, "votes": 47000, "seats":5},
                {"option": "Blanco", "number": 2, "votes": 16000, "seats":2},
                {"option": "Rojo", "number": 3, "votes": 15900, "seats":2},
                {"option": "Verde", "number": 4, "votes": 12000, "seats":1},
                {"option": "Azul", "number": 5, "votes": 6000, "seats":0},
                {"option": "Rosa", "number": 6, "votes": 3100, "seats":0},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )

    def test_sainte_lague(self):
        data = {
            "type": "LAGUE",
            "options": common_options,
        }
        expected_result = [
                {"option": "Amarillo", "number": 1, "votes": 47000, "seats":3},
                {"option": "Blanco", "number": 2, "votes": 16000, "seats":2},
                {"option": "Rojo", "number": 3, "votes": 15900, "seats":2},
                {"option": "Verde", "number": 4, "votes": 12000, "seats":2},
                {"option": "Azul", "number": 5, "votes": 6000, "seats":1},
                {"option": "Rosa", "number": 6, "votes": 3100, "seats":0},
        ]
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(
            sorted(values, key=lambda x: x["option"]),
            sorted(expected_result, key=lambda x: x["option"]),
        )
