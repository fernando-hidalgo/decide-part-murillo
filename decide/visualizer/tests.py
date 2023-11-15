import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from datetime import datetime

from django.contrib.admin.sites import AdminSite
import json


class VisualizerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc="test question")
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option="option {}".format(i + 1))
            opt.save()
        v = Voting(name="test voting", question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(
            url=settings.BASEURL, defaults={"me": True, "name": "test auth"}
        )
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username="testvoter{}".format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = "user{}".format(pk)
        user.set_password("qwerty")
        user.save()
        return user

    # Genera un número de votos concreto para poder contarlos en los tests de visualización
    def store_votes_visualizer(self, v, num_votes=30):
        # Crear votantes aleatorios
        voters = random.sample(list(Census.objects.filter(voting_id=v.id)), num_votes)

        # Crear votos aleatorios
        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for _ in range(num_votes // len(v.question.options.all())):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    "voting": v.id,
                    "voter": voters.pop().voter_id,
                    "vote": {"a": a, "b": b},
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(data["voter"])
                self.login(user=user.username)
                self.client.post("/store/", data, format="json")

        return clear

    def test_visualizer_data(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes_visualizer(v)

        self.login()
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

        response = self.client.get(f"/visualizer/{v.id}/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")

        content = response.content.decode("utf-8")

        self.assertIn("Recuento de votos", content)
        self.assertIn("Total de personas en el censo", content)
        self.assertIn("Porcentaje del censo que ha votado", content)


class Testswitchlanguage:
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def tearDown(self):
        self.driver.quit()

    def test_testswitchlanguage(self):
        self.driver.get("http://localhost:8000/visualizer/2/")
        self.driver.set_window_size(945, 1016)
        dropdown = self.driver.find_element(By.NAME, "language")
        dropdown.find_element(By.XPATH, "//option[. = 'Inglés']").click()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.NAME, "language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
