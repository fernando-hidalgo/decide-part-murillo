from rest_framework import serializers

from .models import (
    Question,
    QuestionYesNo,
    QuestionOption,
    QuestionMultiChoice,
    QuestionOptionMultiChoice,
    QuestionByPreference,
    QuestionOptionByPreference,
    Voting,
    VotingYesNo,
    VotingByPreference,
    VotingMultiChoice,

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

class QuestionOptionMultiChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOptionMultiChoice
        fields = ("number", "option")

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ("desc", "options")

class QuestionYesNoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionYesNo
        fields = ("desc", "optionYes", "optionNo")

class QuestionByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    preferences = QuestionOptionByPreferenceSerializer(many=True)

    class Meta:
        model = QuestionByPreference
        fields = ("desc", "preferences")

class QuestionMultiChoiceSerializer(serializers.HyperlinkedModelSerializer):
    multichoices = QuestionOptionMultiChoiceSerializer(many=True)

    class Meta:
        model = QuestionMultiChoice
        fields = ("desc", "multichoices")

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


class VotingYesNoSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionYesNoSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = VotingYesNo
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

class VotingMultiChoiceSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionMultiChoiceSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = VotingMultiChoice
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

class SimpleVotingYesNoSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionYesNoSerializer(many=False)

    class Meta:
        model = VotingYesNo
        fields = ("name", "desc", "question", "start_date", "end_date")
        
class SimpleVotingByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionByPreferenceSerializer(many=False)

    class Meta:
        model = VotingByPreference
        fields = ("name", "desc", "question", "start_date", "end_date")

class SimpleVotingMultiChoiceSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionMultiChoiceSerializer(many=False)

    class Meta:
        model = VotingMultiChoice
        fields = ("name", "desc", "question", "start_date", "end_date")
