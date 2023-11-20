from rest_framework import serializers

from .models import Vote
from .models import VoteYN


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ("voting_id", "voter_id", "a", "b")


class VoteYNSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()


class Meta:
    model = VoteYN
    fields = ("voting_yesno_id", "voter_yesno_id", "a", "b")
