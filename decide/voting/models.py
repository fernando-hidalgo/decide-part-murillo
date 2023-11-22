from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

from base import mods
from base.models import Auth, Key

class Question(models.Model):
    desc = models.TextField()

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

class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    questions = models.ManyToManyField(Question, related_name="votings")  # Cambiada a ManyToMany

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
        # Obtener votos desde el almacenamiento
        votes = mods.get(
            "store", params={"voting_id": self.id}, HTTP_AUTHORIZATION="Token " + token
        )
        # Votos anónimos
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
        for question in self.questions.all():
            selected_options = question.options.filter(voting=self)
            votes = []

            for option in selected_options:
                votes.extend(option.votes.all())

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
        options = self.questions.first().options.all()

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
