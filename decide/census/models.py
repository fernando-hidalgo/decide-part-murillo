from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (("voting_id", "voter_id", "group"),)


class CensusByPreference(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (('voting_id', 'voter_id', "group"),)
        
class CensusYesNo(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (("voting_id", "voter_id"),)