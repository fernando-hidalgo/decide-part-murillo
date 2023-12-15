from django.db import models
from base.models import BigBigField


class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.voting_id, self.voter_id)


class VoteYN(models.Model):
    voting_yesno_id = models.PositiveIntegerField()
    voter_yesno_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.voting_yesno_id, self.voter_yesno_id)


class VoteByPreference(models.Model):
    voting_preference_id = models.PositiveIntegerField()
    voter_preference_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.voting_preference_id, self.voter_preference_id)

class VoteMultiChoice(models.Model):
    voting_multichoice_id = models.PositiveIntegerField()
    voter_multichoice_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.voting_multichoice_id, self.voter_multichoice_id)
