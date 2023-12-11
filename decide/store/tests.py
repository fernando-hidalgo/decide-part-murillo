import datetime
import random
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import Vote, VoteByPreference, VoteYN
from .serializers import VoteByPreferenceSerializer, VoteSerializer, VoteYNSerializer
from base import mods
from base.models import Auth
from base.tests import BaseTestCase
from census.models import Census, CensusByPreference, CensusYesNo
from mixnet.models import Key
from voting.models import (
    Question,
    QuestionByPreference,
    VotingByPreference,
    QuestionYesNo,
    VotingYesNo,
)
from voting.models import Voting


class StoreTextCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.question = Question(desc="qwerty")
        self.question.save()
        self.voting = Voting(
            pk=5001, 
            name='voting example', 
            start_date=timezone.now()
            )
        self.voting.save()
        self.voting.question.set([self.question])

        self.question_by_preference = QuestionByPreference(desc="qwerty")
        self.question_by_preference.save()
        self.voting_by_preference = VotingByPreference(
            pk=5001,
            name="voting example",
            question=self.question_by_preference,
            start_date=timezone.now(),
        )
        self.voting_by_preference.save()
        # Store de yes no
        self.question_yes_no = QuestionYesNo(desc="qwerty")
        self.question_yes_no.save()
        self.voting_yes_no = VotingYesNo(
            pk=5001,
            name="voting example",
            question=self.question_yes_no,
            start_date=timezone.now(),
        )
        self.voting_yes_no.save()

    def tearDown(self):
        super().tearDown()

    def gen_voting(self, pk):
        voting = Voting(pk=pk, name='v1', start_date=timezone.now(), end_date=timezone.now() + datetime.timedelta(days=1))
        voting.save()
        voting.question.set([self.question])
        voting.save()



    def gen_voting_by_preference(self, pk):
        voting_by_preference = VotingByPreference(
            pk=pk,
            name="v1",
            question=self.question_by_preference,
            start_date=timezone.now(),
            end_date=timezone.now() + datetime.timedelta(days=1),
        )
        voting_by_preference.save()

    def gen_voting_yes_no(self, pk):
        voting_yes_no = VotingYesNo(
            pk=pk,
            name="v1",
            question=self.question_yes_no,
            start_date=timezone.now(),
            end_date=timezone.now() + datetime.timedelta(days=1),
        )
        voting_yes_no.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = "user{}".format(pk)
        user.set_password("qwerty")
        user.save()
        return user

    def gen_votes(self):
        votings = [random.randint(1, 5000) for i in range(10)]
        users = [random.randint(3, 5002) for i in range(50)]
        for v in votings:
            a = random.randint(2, 500)
            b = random.randint(2, 500)
            self.gen_voting(v)
            random_user = random.choice(users)
            user = self.get_or_create_user(random_user)
            self.login(user=user.username)
            census = Census(voting_id=v, voter_id=random_user)
            census.save()
            data = {"voting": v, "voter": random_user, "vote": {"a": a, "b": b}}
            response = self.client.post("/store/", data, format="json")
            self.assertEqual(response.status_code, 200)

        self.logout()
        return votings, users

    def gen_votes_by_preferences(self):
        votings_by_preference = [random.randint(1, 5000) for i in range(10)]
        users = [random.randint(3, 5002) for i in range(50)]
        for v in votings_by_preference:
            a = random.randint(2, 500)
            b = random.randint(2, 500)
            self.gen_voting_by_preference(v)
            random_user = random.choice(users)
            user = self.get_or_create_user(random_user)
            self.login(user=user.username)
            census = CensusByPreference(voting_id=v, voter_id=random_user)
            census.save()
            data = {"voting": v, "voter": random_user, "vote": {"a": a, "b": b}}
            response = self.client.post("/store/preference/", data, format="json")
            self.assertEqual(response.status_code, 200)

        self.logout()
        return votings_by_preference, users

    def gen_votes_yes_no(self):
        votings_yes_no = [random.randint(1, 5000) for i in range(10)]
        users = [random.randint(3, 5002) for i in range(50)]
        for v in votings_yes_no:
            a = random.randint(2, 500)
            b = random.randint(2, 500)
            self.gen_voting_yes_no(v)
            random_user = random.choice(users)
            user = self.get_or_create_user(random_user)
            self.login(user=user.username)
            census = CensusYesNo(voting_id=v, voter_id=random_user)
            census.save()
            data = {"voting": v, "voter": random_user, "vote": {"a": a, "b": b}}
            response = self.client.post("/store/yesno/", data, format="json")
            self.assertEqual(response.status_code, 200)

        self.logout()
        return votings_yes_no, users

    def test_gen_vote_invalid(self):
        data = {"voting": 1, "voter": 1, "vote": {"a": 1, "b": 1}}
        response = self.client.post("/store/", data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_gen_vote_by_preference_invalid(self):
        data = {"voting": 1, "voter": 1, "vote": {"a": 1, "b": 1}}
        response = self.client.post("/store/preference/", data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_gen_vote_yes_no_invalid(self):
        data = {"voting": 1, "voter": 1, "vote": {"a": 1, "b": 1}}
        response = self.client.post("/store/yesno/", data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_store_vote(self):
        VOTING_PK = 345
        CTE_A = 96
        CTE_B = 184
        census = Census(voting_id=VOTING_PK, voter_id=1)
        census.save()
        self.gen_voting(VOTING_PK)
        data = {"voting": VOTING_PK, "voter": 1, "vote": {"a": CTE_A, "b": CTE_B}}
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post("/store/", data, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().voting_id, VOTING_PK)
        self.assertEqual(Vote.objects.first().voter_id, 1)
        self.assertEqual(Vote.objects.first().a, CTE_A)
        self.assertEqual(Vote.objects.first().b, CTE_B)

    def test_store_vote_by_preference(self):
        VOTING_PK = 345
        CTE_A = 96
        CTE_B = 184
        census = CensusByPreference(voting_id=VOTING_PK, voter_id=1)
        census.save()
        self.gen_voting_by_preference(VOTING_PK)
        data = {"voting": VOTING_PK, "voter": 1, "vote": {"a": CTE_A, "b": CTE_B}}
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post("/store/preference/", data, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(VoteByPreference.objects.count(), 1)
        self.assertEqual(
            VoteByPreference.objects.first().voting_preference_id, VOTING_PK
        )
        self.assertEqual(VoteByPreference.objects.first().voter_preference_id, 1)
        self.assertEqual(VoteByPreference.objects.first().a, CTE_A)
        self.assertEqual(VoteByPreference.objects.first().b, CTE_B)

    def test_store_vote_yes_no(self):
        VOTING_PK = 345
        CTE_A = 96
        CTE_B = 184
        census = CensusYesNo(voting_id=VOTING_PK, voter_id=1)
        census.save()
        self.gen_voting_yes_no(VOTING_PK)
        data = {"voting": VOTING_PK, "voter": 1, "vote": {"a": CTE_A, "b": CTE_B}}
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post("/store/yesno/", data, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(VoteYN.objects.count(), 1)
        self.assertEqual(VoteYN.objects.first().voting_yesno_id, VOTING_PK)
        self.assertEqual(VoteYN.objects.first().voter_yesno_id, 1)
        self.assertEqual(VoteYN.objects.first().a, CTE_A)
        self.assertEqual(VoteYN.objects.first().b, CTE_B)

    def test_vote(self):
        self.gen_votes()
        response = self.client.get("/store/", format="json")
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get("/store/", format="json")
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get("/store/", format="json")
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), Vote.objects.count())
        self.assertEqual(votes[0], VoteSerializer(Vote.objects.all().first()).data)

    def test_vote_by_preference(self):
        self.gen_votes_by_preferences()
        response = self.client.get("/store/preference/", format="json")
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get("/store/preference/", format="json")
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get("/store/preference/", format="json")
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), VoteByPreference.objects.count())
        self.assertEqual(
            votes[0],
            VoteByPreferenceSerializer(VoteByPreference.objects.all().first()).data,
        )

    def test_vote_yes_no(self):
        self.gen_votes_yes_no()
        response = self.client.get("/store/yesno/", format="json")
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get("/store/yesno/", format="json")
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get("/store/yesno/", format="json")
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), VoteYN.objects.count())
        self.assertEqual(
            votes[0],
            VoteYNSerializer(VoteYN.objects.all().first()).data,
        )

    def test_filter(self):
        votings, voters = self.gen_votes()
        v = votings[0]

        response = self.client.get("/store/?voting_id={}".format(v), format="json")
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get("/store/?voting_id={}".format(v), format="json")
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get("/store/?voting_id={}".format(v), format="json")
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), Vote.objects.filter(voting_id=v).count())

        v = voters[0]
        response = self.client.get("/store/?voter_id={}".format(v), format="json")
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), Vote.objects.filter(voter_id=v).count())

    def test_filter_by_preference(self):
        votings, voters = self.gen_votes_by_preferences()
        v = votings[0]

        response = self.client.get(
            "/store/preference/?voting_preference_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get(
            "/store/preference/?voting_preference_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get(
            "/store/preference/?voting_preference_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(
            len(votes), VoteByPreference.objects.filter(voting_preference_id=v).count()
        )

        v = voters[0]
        response = self.client.get(
            "/store/preference/?voter_preference_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(
            len(votes), VoteByPreference.objects.filter(voter_preference_id=v).count()
        )

    def test_filter_yes_no(self):
        votings, voters = self.gen_votes_yes_no()
        v = votings[0]

        response = self.client.get(
            "/store/yesno/?voting_preference_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get(
            "/store/yesno/?voting_yesno_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get(
            "/store/yesno/?voting_yesno_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), VoteYN.objects.filter(voting_yesno_id=v).count())

        v = voters[0]
        response = self.client.get(
            "/store/preference/?voter_preference_id={}".format(v), format="json"
        )
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(
            len(votes), VoteByPreference.objects.filter(voter_preference_id=v).count()
        )

    def test_hasvote(self):
        votings, voters = self.gen_votes()
        vo = Vote.objects.first()
        v = vo.voting_id
        u = vo.voter_id

        response = self.client.get(
            "/store/?voting_id={}&voter_id={}".format(v, u), format="json"
        )
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get(
            "/store/?voting_id={}&voter_id={}".format(v, u), format="json"
        )
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get(
            "/store/?voting_id={}&voter_id={}".format(v, u), format="json"
        )
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0]["voting_id"], v)
        self.assertEqual(votes[0]["voter_id"], u)

    def test_hasvote_by_preference(self):
        votings, voters = self.gen_votes_by_preferences()
        vo = VoteByPreference.objects.first()
        v = vo.voting_preference_id
        u = vo.voter_preference_id

        response = self.client.get(
            "/store/preference/?voting_preference_id={}&voter_preference_id={}".format(
                v, u
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get(
            "/store/preference/?voting_preference_id={}&voter_preference_id={}".format(
                v, u
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get(
            "/store/preference/?voting_preference_id={}&voter_preference_id={}".format(
                v, u
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0]["voting_preference_id"], v)
        self.assertEqual(votes[0]["voter_preference_id"], u)

    def test_hasvote_yes_no(self):
        votings, voters = self.gen_votes_yes_no()
        vo = VoteYN.objects.first()
        v = vo.voting_yesno_id
        u = vo.voter_yesno_id

        response = self.client.get(
            "/store/yesno/?voting_yesno_id={}&voter_yesno_id={}".format(v, u),
            format="json",
        )
        self.assertEqual(response.status_code, 401)

        self.login(user="noadmin")
        response = self.client.get(
            "/store/yesno/?voting_yesno_id={}&voter_yesno_id={}".format(v, u),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get(
            "/store/yesno/?voting_yesno_id={}&voter_yesno_id={}".format(v, u),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0]["voting_yesno_id"], v)
        self.assertEqual(votes[0]["voter_yesno_id"], u)

    def test_voting_status(self):
        data = {"voting": 5001, "voter": 1, "vote": {"a": 30, "b": 55}}
        census = Census(voting_id=5001, voter_id=1)
        census.save()
        # not opened
        self.voting.start_date = timezone.now() + datetime.timedelta(days=1)
        self.voting.save()
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post("/store/", data, format="json")
        self.assertEqual(response.status_code, 401)

        # not closed
        self.voting.start_date = timezone.now() - datetime.timedelta(days=1)
        self.voting.save()
        self.voting.end_date = timezone.now() + datetime.timedelta(days=1)
        self.voting.save()
        response = self.client.post("/store/", data, format="json")
        self.assertEqual(response.status_code, 200)

        # closed
        self.voting.end_date = timezone.now() - datetime.timedelta(days=1)
        self.voting.save()
        response = self.client.post("/store/", data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_voting_by_preference_status(self):
        data = {"voting": 5001, "voter": 1, "vote": {"a": 30, "b": 55}}
        census = CensusByPreference(voting_id=5001, voter_id=1)
        census.save()
        # not opened
        self.voting_by_preference.start_date = timezone.now() + datetime.timedelta(
            days=1
        )
        self.voting_by_preference.save()
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post("/store/preference/", data, format="json")
        self.assertEqual(response.status_code, 401)

        # not closed
        self.voting_by_preference.start_date = timezone.now() - datetime.timedelta(
            days=1
        )
        self.voting_by_preference.save()
        self.voting_by_preference.end_date = timezone.now() + datetime.timedelta(days=1)
        self.voting_by_preference.save()
        response = self.client.post("/store/preference/", data, format="json")
        self.assertEqual(response.status_code, 200)

        # closed
        self.voting_by_preference.end_date = timezone.now() - datetime.timedelta(days=1)
        self.voting_by_preference.save()
        response = self.client.post("/store/preference/", data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_voting_yes_no_status(self):
        data = {"voting": 5001, "voter": 1, "vote": {"a": 30, "b": 55}}
        census = CensusYesNo(voting_id=5001, voter_id=1)
        census.save()
        # not opened
        self.voting_yes_no.start_date = timezone.now() + datetime.timedelta(days=1)
        self.voting_yes_no.save()
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post("/store/yesno/", data, format="json")
        self.assertEqual(response.status_code, 401)

        # not closed
        self.voting_yes_no.start_date = timezone.now() - datetime.timedelta(days=1)
        self.voting_yes_no.save()
        self.voting_yes_no.end_date = timezone.now() + datetime.timedelta(days=1)
        self.voting_yes_no.save()
        response = self.client.post("/store/yesno/", data, format="json")
        self.assertEqual(response.status_code, 200)

        # closed
        self.voting_yes_no.end_date = timezone.now() - datetime.timedelta(days=1)
        self.voting_yes_no.save()
        response = self.client.post("/store/yesno/", data, format="json")
        self.assertEqual(response.status_code, 401)
