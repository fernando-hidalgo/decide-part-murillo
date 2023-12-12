from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse

from base import mods


class AuthTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username="voter1")
        u.set_password("123")
        u.save()

        u2 = User(username="admin")
        u2.set_password("admin")
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {"username": "voter1", "password": "123"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get("token"))

    def test_login_fail(self):
        data = {"username": "voter1", "password": "321"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {"username": "voter1", "password": "123"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post("/authentication/getuser/", token, format="json")
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user["id"], 1)
        self.assertEqual(user["username"], "voter1")

    def test_getuser_invented_token(self):
        token = {"token": "invented"}
        response = self.client.post("/authentication/getuser/", token, format="json")
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {"username": "voter1", "password": "123"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username="voter1").count(), 1)

        token = response.json()
        self.assertTrue(token.get("token"))

        response = self.client.post("/authentication/logout/", token, format="json")
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/authentication/getuser/", token, format="json")
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {"username": "voter1", "password": "123"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username="voter1").count(), 1)

        token = response.json()
        self.assertTrue(token.get("token"))

        response = self.client.post("/authentication/logout/", token, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username="voter1").count(), 0)

    def test_register_bad_permissions(self):
        data = {"username": "voter1", "password": "123"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({"username": "user1"})
        response = self.client.post("/authentication/register/", token, format="json")
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {"username": "admin", "password": "admin"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({"username": "user1"})
        response = self.client.post("/authentication/register/", token, format="json")
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {"username": "admin", "password": "admin"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post("/authentication/register/", token, format="json")
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {"username": "admin", "password": "admin"}
        response = self.client.post("/authentication/login/", data, format="json")
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({"username": "user1", "password": "pwd1"})
        response = self.client.post("/authentication/register/", token, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(sorted(list(response.json().keys())), ["token", "user_pk"])

    def test_register_user_get_page(self):
        url = "/authentication/registeruser/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_user_success(self):
        url = "/authentication/registeruser/"
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "thispasswordisactuallysecure123",
            "password_conf": "thispasswordisactuallysecure123",
        }

        response = self.client.post(url, data)

        url = reverse("home")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
        self.assertTrue(User.objects.filter(username="new_user").exists())
        self.assertTrue(Token.objects.filter(user__username="new_user").exists())

    def test_register_username_exists(self):
        url = "/authentication/registeruser/"
        self.assertTrue(User.objects.filter(username="voter1").exists())
        data = {
            "username": "voter1",
            "email": "new_user@example.com",
            "password": "thispasswordisactuallysecure123",
            "password_conf": "thispasswordisactuallysecure123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Username already exists. Please choose a different username."
        )

    def test_register_short_password(self):
        url = "/authentication/registeruser/"
        data = {
            "username": "user1",
            "email": "new_user@example.com",
            "password": "A7iN6Gr",
            "password_conf": "A7iN6Gr",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password must contain at least 8 characters.")
        self.assertFalse(User.objects.filter(username="user1").exists())

    def test_register_digit_password(self):
        url = "/authentication/registeruser/"
        data = {
            "username": "user1",
            "email": "new_user@example.com",
            "password": "2746724732476427641761",
            "password_conf": "2746724732476427641761",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Password cannot be entirely numeric. Please include alphabetic or special characters.",
        )
        self.assertFalse(User.objects.filter(username="user1").exists())

    def test_register_different_password(self):
        url = "/authentication/registeruser/"
        data = {
            "username": "user1",
            "email": "new_user@example.com",
            "password": "ASanspid31240HBAD",
            "password_conf": "A7iN6Grwtwret",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match. Please try again.")
        self.assertFalse(User.objects.filter(username="user1").exists())

    def test_register_common_password(self):
        url = "/authentication/registeruser/"
        data = {
            "username": "user1",
            "email": "new_user@example.com",
            "password": "password1234",
            "password_conf": "password1234",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Password is commonly used. Please choose a different password."
        )
        self.assertFalse(User.objects.filter(username="user1").exists())

    def test_register_password_similar_to_username(self):
        url = "/authentication/registeruser/"
        data = {
            "username": "asgrhsoifdhg234653",
            "email": "new_user@example.com",
            "password": "asgrhsoifdhg23465312",
            "password_conf": "asgrhsoifdhg23465312",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Password cannot be similar to the username. Please choose a different password.",
        )
        self.assertFalse(User.objects.filter(username="user1").exists())
