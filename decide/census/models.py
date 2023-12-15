from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from voting.models import Voting
from django.contrib.auth.models import User

class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (("voting_id", "voter_id", "group"),)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            voter_id = self.voter_id
            voting_id = self.voting_id
            send_confirmation_email(self= self,user_id=voter_id, voting_id=voting_id, voting_type="Normal")



class CensusByPreference(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (('voting_id', 'voter_id', "group"),)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            voter_id = self.voter_id
            voting_id = self.voting_id
            send_confirmation_email(self= self,user_id=voter_id, voting_id=voting_id, voting_type="Por preferencia")
        
class CensusYesNo(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (("voting_id", "voter_id"),)

class CensusMultiChoice(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (('voting_id', 'voter_id', 'group'),)