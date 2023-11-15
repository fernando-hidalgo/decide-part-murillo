from rest_framework import serializers

from .models import (
    Question,
    QuestionByPreference,
    QuestionOption,
    QuestionOptionByPreference,
    Voting,
    VotingByPreference,
)
from base.serializers import KeySerializer, AuthSerializer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ("number", "option")


class QuestionOptionByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOptionByPreference
        fields = ("number", "option", "preference")


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ("desc", "options")


class QuestionByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    preferences = QuestionOptionByPreferenceSerializer(many=True)

    class Meta:
        model = QuestionByPreference
        fields = ("desc", "preferences")


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = (
            "id",
            "name",
            "desc",
            "question",
            "start_date",
            "end_date",
            "pub_key",
            "auths",
            "tally",
            "postproc",
        )


class VotingByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionByPreferenceSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = VotingByPreference
        fields = (
            "id",
            "name",
            "desc",
            "question",
            "start_date",
            "end_date",
            "pub_key",
            "auths",
            "tally",
            "postproc",
        )


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ("name", "desc", "question", "start_date", "end_date")


class SimpleVotingByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionByPreferenceSerializer(many=False)

    class Meta:
        model = VotingByPreference
        fields = ("name", "desc", "question", "start_date", "end_date")
