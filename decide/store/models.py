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


class VoteByPreference(models.Model):
    voting_preference_id = models.PositiveIntegerField()
    voter_preference_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.voting_preference_id, self.voter_preference_id)
