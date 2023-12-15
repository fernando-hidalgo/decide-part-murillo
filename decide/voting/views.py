import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import (
    Question,
    QuestionByPreference,
    QuestionOption,
    QuestionOptionByPreference,
    QuestionYesNo,
    QuestionMultiChoice,
    QuestionOptionMultiChoice,
    Voting,
    VotingByPreference,
    VotingYesNo,
    VotingMultiChoice,
)
from .serializers import (
    SimpleVotingByPreferenceSerializer,
    SimpleVotingSerializer,
    SimpleVotingYesNoSerializer,
    SimpleVotingMultiChoiceSerializer,
    VotingByPreferenceSerializer,
    VotingSerializer,
    VotingYesNoSerializer,
    VotingMultiChoiceSerializer,

)
from base.perms import UserIsStaff
from base.models import Auth


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("id",)

    def get(self, request, *args, **kwargs):
        idpath = kwargs.get("voting_id")
        self.queryset = Voting.objects.all()
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == "v2":
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ["name", "desc", "question", "question_opt"]:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get("question"))
        question.save()
        for idx, q_opt in enumerate(request.data.get("question_opt")):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(
            name=request.data.get("name"),
            desc=request.data.get("desc"),
            question=question,
        )
        voting.save()

        auth, _ = Auth.objects.get_or_create(
            url=settings.BASEURL, defaults={"me": True, "name": "test auth"}
        )
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get("action")
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ""
        st = status.HTTP_200_OK
        if action == "start":
            if voting.start_date:
                msg = "Voting already started"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = "Voting started"
        elif action == "stop":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = "Voting already stopped"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = "Voting stopped"
        elif action == "tally":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = "Voting is not stopped"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = "Voting already tallied"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = "Voting tallied"
        else:
            msg = "Action not found, try with start, stop or tally"
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)


class VotingYNView(generics.ListCreateAPIView):
    queryset = VotingYesNo.objects.all()
    serializer_class = VotingYesNoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("id",)

    def get(self, request, *args, **kwargs):
        idpath = kwargs.get("voting_yesno_id")
        self.queryset = VotingYesNo.objects.all()
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == "v2":
            self.serializer_class = SimpleVotingYesNoSerializer

        return super().get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ["name", "desc", "question"]:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = QuestionYesNo(desc=request.data.get("question"))
        question.save()
        voting = VotingYesNo(
            name=request.data.get("name"),
            desc=request.data.get("desc"),
            question=question,
        )
        voting.save()

        auth, _ = Auth.objects.get_or_create(
            url=settings.BASEURL, defaults={"me": True, "name": "test auth"}
        )
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingByPreferenceView(generics.ListCreateAPIView):
    queryset = VotingByPreference.objects.all()
    serializer_class = VotingByPreferenceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("id",)

    def get(self, request, *args, **kwargs):
        idpath = kwargs.get("voting_by_preference_id")
        self.queryset = VotingByPreference.objects.all()
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == "v2":
            self.serializer_class = SimpleVotingByPreferenceSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)

        for data in ["name", "desc", "question", "question_opt"]:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = QuestionByPreference(desc=request.data.get("question"))
        question.save()
        for idx, q_opt in enumerate(request.data.get("question_opt")):
            opt = QuestionOptionByPreference(
                question=question, option=q_opt, number=idx, preference=idx
            )
            opt.save()
        voting = VotingByPreference(
            name=request.data.get("name"),
            desc=request.data.get("desc"),
            question=question,
        )
        voting.save()

        auth, _ = Auth.objects.get_or_create(
            url=settings.BASEURL, defaults={"me": True, "name": "test auth"}
        )
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)

class VotingMultiChoiceView(generics.ListCreateAPIView):
    queryset = VotingMultiChoice.objects.all()
    serializer_class = VotingMultiChoiceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("id",)

    def get(self, request, *args, **kwargs):
        idpath = kwargs.get("voting_multichoice_id")
        self.queryset = VotingMultiChoice.objects.all()
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == "v2":
            self.serializer_class = SimpleVotingMultiChoiceSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ["name", "desc", "question", "question_opt"]:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = QuestionMultiChoice(desc=request.data.get("question"))
        question.save()

        selected_options = []
        for idx, q_opt in enumerate(request.data.get("question_opt")):
            opt = QuestionOptionMultiChoice(question=question, option=q_opt, number=idx, multichoice=idx)
            opt.save()

        voting = VotingMultiChoice(
            name=request.data.get("name"),
            desc=request.data.get("desc"),
            question=question,
        )
        voting.save()

        auth, _ = Auth.objects.get_or_create(
            url=settings.BASEURL, defaults={"me": True, "name": "test auth"}
        )
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingYesNoUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = VotingYesNo.objects.all()
    serializer_class = VotingYesNoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_yes_no_id, *args, **kwars):
        action = request.data.get("action")
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(VotingYesNo, pk=voting_yes_no_id)
        msg = ""
        st = status.HTTP_200_OK
        if action == "start":
            if voting.start_date:
                msg = "Voting already started"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = "Voting started"
        elif action == "stop":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = "Voting already stopped"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = "Voting stopped"
        elif action == "tally":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = "Voting is not stopped"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = "Voting already tallied"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = "Voting tallied"
        else:
            msg = "Action not found, try with start, stop or tally"
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)


class VotingByPreferenceUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = VotingByPreference.objects.all()
    serializer_class = VotingByPreferenceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_by_preference_id, *args, **kwars):
        action = request.data.get("action")
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(VotingByPreference, pk=voting_by_preference_id)
        msg = ""
        st = status.HTTP_200_OK
        if action == "start":
            if voting.start_date:
                msg = "Voting already started"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = "Voting started"
        elif action == "stop":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = "Voting already stopped"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = "Voting stopped"
        elif action == "tally":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = "Voting is not stopped"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = "Voting already tallied"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = "Voting tallied"
        else:
            msg = "Action not found, try with start, stop or tally"
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)

class VotingMultiChoiceUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = VotingMultiChoice.objects.all()
    serializer_class = VotingMultiChoiceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_multichoice_id, *args, **kwars):
        action = request.data.get("action")
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(VotingMultiChoice, pk=voting_multichoice_id)
        msg = ""
        st = status.HTTP_200_OK
        if action == "start":
            if voting.start_date:
                msg = "Voting already started"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = "Voting started"
        elif action == "stop":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = "Voting already stopped"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = "Voting stopped"
        elif action == "tally":
            if not voting.start_date:
                msg = "Voting is not started"
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = "Voting is not stopped"
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = "Voting already tallied"
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = "Voting tallied"
        else:
            msg = "Action not found, try with start, stop or tally"
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)