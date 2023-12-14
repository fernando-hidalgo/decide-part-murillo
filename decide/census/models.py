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
        
class CensusYesNo(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (("voting_id", "voter_id"),)

def send_confirmation_email(self, user_id, voting_id, voting_type):
        try:
            user = User.objects.get(id=user_id)
            voting = Voting.objects.get(id=voting_id)
            subject = 'Añadido a votación '+ voting_type
            from_email = 'piezasrevive@outlook.com'
            to_email = [user.email] 
            username = user.username
            first_name = user.first_name
            last_name = user.last_name
            name = voting.name
            desc = voting.desc
            start_date = voting.start_date
            end_date = voting.end_date
            context = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "name": name,
                "desc": desc,
                "start_date": start_date,
                "end_date": end_date,
            }

            html_message = render_to_string('census/aviso.html', context)
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(
                subject,
                plain_message,
                from_email,
                to_email
            )

            email.attach_alternative(html_message, "text/html")
            email.send()
        except Exception as e:
            print(f"Error al enviar el correo: {e}")