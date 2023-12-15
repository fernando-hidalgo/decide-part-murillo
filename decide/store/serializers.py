from rest_framework import serializers

from .models import Vote
from .models import VoteYN
from .models import VoteByPreference
from .models import VoteMultiChoice


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


class VoteByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = VoteByPreference
        fields = ("voting_preference_id", "voter_preference_id", "a", "b")

class VoteMultiChoiceSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = VoteMultiChoice
        fields = ("voting_multichoice_id", "voter_multichoice_id", "a", "b")