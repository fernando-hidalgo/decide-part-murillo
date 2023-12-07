from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from store.models import Vote, VoteYN

from base import mods
from base.models import Auth, Key
from store.models import VoteByPreference


class QuestionByPreference(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


# Modelo para preguntas de tipo si o no
class QuestionYesNo(models.Model):
    desc = models.TextField()

    optionYes = models.PositiveIntegerField(editable=False, default=1)
    optionNo = models.PositiveIntegerField(editable=False, default=2)

    def save(self, *args, **kwargs):
        self.optionYes = 1
        self.optionNo = 2
        super().save(*args, **kwargs)

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question, related_name="options", on_delete=models.CASCADE
    )
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return "{} ({})".format(self.option, self.number)


# Modelo para preguntas de tipo si o no
class QuestionOptionYesNo(models.Model):
    question = models.ForeignKey(
        QuestionYesNo, related_name="pregYN", on_delete=models.CASCADE
    )

    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()
    option = models.PositiveIntegerField(blank=True, null=True)

    def save(self):

        self.preference = 0
        if not self.number:
            self.number = self.question.pregYN.count() + 2
        return super().save()

    def str(self):
        return "{} ({})".format(self.option, self.number)


class QuestionOptionByPreference(models.Model):
    question = models.ForeignKey(
        QuestionByPreference, related_name="preferences", on_delete=models.CASCADE
    )
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()
    preference = models.PositiveIntegerField(blank=True, null=True)

    def save(self):

        self.preference = 0
        if not self.number:
            self.number = self.question.preferences.count() + 2
        return super().save()

    def __str__(self):
        return "{} ({})".format(self.option, self.number)


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(
        Question, related_name="voting", on_delete=models.CASCADE
    )

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(
        Key, related_name="voting", blank=True, null=True, on_delete=models.SET_NULL
    )
    auths = models.ManyToManyField(Auth, related_name="votings")

    tallyType = models.CharField(max_length=200, default="IDENTITY")
    escaños = models.IntegerField(default=10)
    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [{"name": a.name, "url": a.url} for a in self.auths.all()],
        }
        key = mods.post("mixnet", baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=""):
        # gettings votes from store
        votes = mods.get(
            "store", params={"voting_id": self.id}, HTTP_AUTHORIZATION="Token " + token
        )
        # anon votes
        votes_format = []
        vote_list = []
        for vote in votes:
            for info in vote:
                if info == "a":
                    votes_format.append(vote[info])
                if info == "b":
                    votes_format.append(vote[info])
            vote_list.append(votes_format)
            votes_format = []
        return vote_list

    def tally_votes(self, token=""):
        """
        The tally is a shuffle and then a decrypt
        """

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = {"msgs": votes}
        response = mods.post(
            "mixnet",
            entry_point=shuffle_url,
            baseurl=auth.url,
            json=data,
            response=True,
        )
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post(
            "mixnet",
            entry_point=decrypt_url,
            baseurl=auth.url,
            json=data,
            response=True,
        )

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append(
                {
                    "option": opt.option,
                    "number": opt.number,
                    "votes": votes,
                }
            )

        data = {"escaños": self.escaños, "type": self.tallyType, "options": opts}
        postp = mods.post("postproc", json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name


# Modelo para votaciones de tipo si o no
class VotingYesNo(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(
        QuestionYesNo, related_name="votingyesno", on_delete=models.CASCADE
    )

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(
        Key,
        related_name="votingyesno",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    auths = models.ManyToManyField(Auth, related_name="votingsyesno")

    tallyType = models.CharField(max_length=200, default="IDENTITY")
    escaños = models.IntegerField(default=10)

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [{"name": a.name, "url": a.url} for a in self.auths.all()],
        }
        key = mods.post("mixnet", baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=""):
        # gettings votes from store
        votes = mods.get(
            "store",
            params={"voting_id": self.id},
            HTTP_AUTHORIZATION="Token " + token,
        )

        # anon votes
        votes_format = []
        vote_list = []
        for vote in votes:
            for info in vote:
                if info == "a":
                    votes_format.append(vote[info])
                if info == "b":
                    votes_format.append(vote[info])
            vote_list.append(votes_format)
            votes_format = []
        return vote_list

    def tally_votes(self, token=""):
        """
        The tally is a shuffle and then a decrypt
        """

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = {"msgs": votes}
        response = mods.post(
            "mixnet",
            entry_point=shuffle_url,
            baseurl=auth.url,
            json=data,
            response=True,
        )
        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.pregYN.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(int(opt))
            else:
                votes = 0
            if int(opt) == 1:
                opts.append({"option": "Si", "votes": votes, "number": 1})
            else:
                opts.append({"option": "No", "votes": votes, "number": 0})

        data = {"escaños": self.escaños, "type": self.tallyType, "options": opts}
        postp = mods.post("postproc", json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name


class VotingByPreference(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(
        QuestionByPreference,
        related_name="votingbypreference",
        on_delete=models.CASCADE,
    )

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(
        Key,
        related_name="votingbypreference",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    auths = models.ManyToManyField(Auth, related_name="votingsbypreference")

    tallyType = models.CharField(max_length=200, default="IDENTITY")
    escaños = models.IntegerField(default=10)

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [{"name": a.name, "url": a.url} for a in self.auths.all()],
        }
        key = mods.post("mixnet", baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=""):
        # gettings votes from store
        auxvoting = VoteByPreference.objects.filter(voting_preference_id=self.id)
        votes = []
        for vote in auxvoting:
            voting_data = {
                "id": vote.id,
                "voting_preference_id": vote.voting_preference_id,
                "voter_preference_id": vote.voter_preference_id,
                "a": vote.a,
                "b": vote.b,
            }
            votes.append(voting_data)
        # anon votes
        votes_format = []
        vote_list = []
        for vote in votes:
            for info in vote:
                if info == "a":
                    votes_format.append(vote[info])
                if info == "b":
                    votes_format.append(vote[info])
            vote_list.append(votes_format)
            votes_format = []
        return vote_list

    def tally_votes(self, token=""):
        """
        The tally is a shuffle and then a decrypt
        """

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = {"msgs": votes}
        response = mods.post(
            "mixnet",
            entry_point=shuffle_url,
            baseurl=auth.url,
            json=data,
            response=True,
        )
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post(
            "mixnet",
            entry_point=decrypt_url,
            baseurl=auth.url,
            json=data,
            response=True,
        )

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        opts = []
        diccionario_preferences = {}
        options = self.question.preferences.all()
        if isinstance(tally, list):
            for t in range(len(tally)):
                tally_str = str(tally[t])
                tally_str_with_commas = tally_str.replace("10000", ",")
                tally_list = [
                    int(num) for num in tally_str_with_commas.split(",") if num
                ]
                for opt in options:
                    key = opt.number
                    if key in diccionario_preferences:
                        diccionario_preferences[key] += tally_list[opt.number - 1]
                    else:
                        diccionario_preferences[key] = tally_list[opt.number - 1]

        for key in diccionario_preferences:
            votes = diccionario_preferences[key]
            votes = votes / len(tally)
            option = options.get(number=key)
            opts.append({"option": option.option, "number": key, "votes": votes})

        data = {"escaños": self.escaños, "type": self.tallyType, "options": opts}
        postp = mods.post("postproc", json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
