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
from census.models import Census, CensusByPreference
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import (
    QuestionByPreference,
    QuestionOptionByPreference,
    Voting,
    Question,
    QuestionOption,
    VotingByPreference,
)
from datetime import datetime

from django.contrib.admin.sites import AdminSite
import json

from django.urls import reverse
from django.utils.translation import activate


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

    def create_voting_by_preference(self):
        q = QuestionByPreference(desc="test question")
        q.save()
        for i in range(4):
            opt = QuestionOptionByPreference(
                question=q, option="option {}".format(i + 1)
            )
            opt.save()
        v = VotingByPreference(name="test voting", question=q)
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

    def create_voters_by_preference(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username="testvoter{}".format(i))
            u.is_active = True
            u.save()
            c = CensusByPreference(voter_id=u.id, voting_id=v.id)
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

    # Genera un número de votos concreto para poder contarlos en los tests de visualización
    def store_votes_preference_visualizer(self, v, num_votes=30):
        # Crear votantes aleatorios
        voters = random.sample(
            list(CensusByPreference.objects.filter(voting_id=v.id)), num_votes
        )

        # Crear votos
        clear = {}
        for opt in v.question.preferences.all():
            clear[opt.number] = 0
            for _ in range(num_votes // len(v.question.preferences.all())):
                a, b = self.encrypt_msg(100004100002100001100003, v)
                data = {
                    "voting": v.id,
                    "voter": voters.pop().voter_id,
                    "vote": {"a": a, "b": b},
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(data["voter"])
                self.login(user=user.username)
                self.client.post("/store/preference/", data, format="json")

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

        response_post = self.client.post(reverse("set_language"), {"language": "es"})
        self.assertEqual(response_post.status_code, 302)  # aseguro que esté en español

        response = self.client.get(f"/visualizer/{v.id}/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")

        content = response.content.decode("utf-8")

        self.assertIn("Recuento de votos", content)
        self.assertIn("Total de personas en el censo", content)
        self.assertIn("Porcentaje del censo que ha votado", content)

    def test_visualizer_preference_data(self):
        v = self.create_voting_by_preference()
        self.create_voters_by_preference(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        self.login()
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

        response_post = self.client.post(reverse("set_language"), {"language": "es"})
        self.assertEqual(response_post.status_code, 302)  # aseguro que esté en español

        response = self.client.get(f"/visualizer/preference/{v.id}/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")

        content = response.content.decode("utf-8")

        self.assertIn("Recuento de votos", content)
        self.assertIn("Total de personas en el censo", content)
        self.assertIn("Porcentaje del censo que ha votado", content)

    def testSwitchToSpanish(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes_visualizer(v)

        self.login()

        response_post = self.client.post(reverse("set_language"), {"language": "es"})
        self.assertEqual(response_post.status_code, 302)

        response = self.client.get(f"/visualizer/{v.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Español")
        self.assertContains(
            response,
            '<form action="/i18n/setlang/" method="post" style="display: inline;">',
        )
        # self.assertContains(response, '<select name="language" onchange="javascript:form.submit()">')
        self.assertContains(response, '<option value="en" >Inglés</option>')
        # self.assertContains(response, '<option value="es" selected="selected">Español</option>')

        html_content = response.content.decode("utf-8")
        self.assertIn("Resultados:", html_content)

    def testSwitchToEnglish(self):
        v = self.create_voting_by_preference()
        self.create_voters_by_preference(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        self.login()

        response_post = self.client.post(reverse("set_language"), {"language": "en"})
        self.assertEqual(response_post.status_code, 302)

        response = self.client.get(f"/visualizer/preference/{v.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "English")
        self.assertContains(
            response,
            '<form action="/i18n/setlang/" method="post" style="display: inline;">',
        )
        # self.assertContains(response, '<select name="language" onchange="javascript:form.submit()">')
        self.assertContains(response, '<option value="es" >Spanish</option>')
        # self.assertContains(response, '<option value="es" selected="selected">Español</option>')

        html_content = response.content.decode("utf-8")
        self.assertIn("Results:", html_content)
