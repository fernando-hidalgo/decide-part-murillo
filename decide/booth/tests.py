from django.test import TestCase
from base.tests import BaseTestCase


# Create your tests here.


class BoothTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testBoothNotFound(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/10000/")
        self.assertEqual(response.status_code, 404)

    def testBoothRedirection(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/10000")
        self.assertEqual(response.status_code, 301)

    def testBoothPreferenceNotFound(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/preference/10000/")
        self.assertEqual(response.status_code, 404)

    def testBoothPreferenceRedirection(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/preference/10000")
        self.assertEqual(response.status_code, 301)

    def testBoothYesNONotFound(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/yesno/10000/")
        self.assertEqual(response.status_code, 404)

    def testBoothYesNoRedirection(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/yesno/10000")
        self.assertEqual(response.status_code, 301)

    def testBoothMultiChoiceNotFound(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/multichoice/10000/")
        self.assertEqual(response.status_code, 404)

    def testBoothMultiChoiceRedirection(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get("/booth/multichoice/10000")
        self.assertEqual(response.status_code, 301)