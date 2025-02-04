from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .models import Vote, VoteYN, VoteMultiChoice
from .serializers import VoteSerializer, VoteYNSerializer
from .models import Vote, VoteByPreference, VoteMultiChoice
from .serializers import VoteByPreferenceSerializer, VoteSerializer, VoteMultiChoiceSerializer
from base import mods
from base.perms import UserIsStaff
from voting.models import VotingYesNo, VotingMultiChoice


class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("voting_id", "voter_id")

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
        * voting: id
        * voter: id
        * vote: { "a": int, "b": int }
        """

        vid = request.data.get("voting")
        voting = mods.get("voting", params={"id": vid})
        if not voting or not isinstance(voting, list):
            # print("por aqui 35")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get("start_date", None)
        # print ("Start date: "+  start_date)
        end_date = voting[0].get("end_date", None)
        # print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        # print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            # print("por aqui 42")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get("voter")
        vote = request.data.get("vote")

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post(
            "authentication", entry_point="/getuser/", json={"token": token}
        )
        voter_id = voter.get("id", None)
        if not voter_id or voter_id != uid:
            # print("por aqui 59")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get(
            "census/{}".format(vid), params={"voter_id": uid}, response=True
        )
        if perms.status_code == 401:
            # print("por aqui 65")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")

        defs = {"a": a, "b": b}
        v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid, defaults=defs)
        v.a = a
        v.b = b

        v.save()

        return Response({})


class StoreYNView(generics.ListAPIView):
    queryset = VoteYN.objects.all()
    serializer_class = VoteYNSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("voting_yesno_id", "voter_yesno_id")

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
        * voting: id
        * voter: id
        * vote: { "a": int, "b": int }
        """

        vid = request.data.get("voting")
        voting = mods.get("voting/yesno", params={"id": vid})
        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        start_date = voting[0].get("start_date", None)
        # print ("Start date: "+  start_date)
        end_date = voting[0].get("end_date", None)
        # print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        # print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            # print("por aqui 42")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get("voter")
        vote = request.data.get("vote")

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post(
            "authentication", entry_point="/getuser/", json={"token": token}
        )

        voter_id = voter.get("id", None)
        if not voter_id or voter_id != uid:
            # print("por aqui 59")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get(
            "census/yesno/{}".format(vid), params={"voter_id": uid}, response=True
        )
        if perms.status_code == 401:
            # print("por aqui 65")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")

        defs = {"a": a, "b": b}
        v, _ = VoteYN.objects.get_or_create(
            voting_yesno_id=vid, voter_yesno_id=uid, defaults=defs
        )
        v.a = a
        v.b = b

        v.save()

        return Response({})


class StoreByPreferenceView(generics.ListAPIView):
    queryset = VoteByPreference.objects.all()
    serializer_class = VoteByPreferenceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("voting_preference_id", "voter_preference_id")

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
        * voting: id
        * voter: id
        * vote: { "a": int, "b": int }
        """
        vid = request.data.get("voting")
        voting_preference = mods.get("voting/preference", params={"id": vid})
        if not voting_preference or not isinstance(voting_preference, list):
            # print("por aqui 35")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting_preference[0].get("start_date", None)
        # print ("Start date: "+  start_date)
        end_date = voting_preference[0].get("end_date", None)
        # print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        # print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            # print("por aqui 42")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get("voter")
        vote = request.data.get("vote")

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post(
            "authentication", entry_point="/getuser/", json={"token": token}
        )

        voter_id = voter.get("id", None)
        if not voter_id or voter_id != uid:
            # print("por aqui 59")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get(
            "census/bypreference/{}".format(vid),
            params={"voter_id": uid},
            response=True,
        )
        if perms.status_code == 401:
            # print("por aqui 65")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")

        defs = {"a": a, "b": b}
        v, _ = VoteByPreference.objects.get_or_create(
            voting_preference_id=vid, voter_preference_id=uid, defaults=defs
        )
        v.a = a
        v.b = b

        v.save()

        return Response({})

class StoreMultiChoiceView(generics.ListAPIView):
    queryset = VoteMultiChoice.objects.all()
    serializer_class = VoteMultiChoiceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ("voting_multichoice_id", "voter_multichoice_id")

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
        * voting: id
        * voter: id
        * vote: { "a": int, "b": int }
        """
        vid = request.data.get("voting")
        voting_multichoice = mods.get("voting/multichoice", params={"id": vid})
        if not voting_multichoice or not isinstance(voting_multichoice, list):
            # print("por aqui 35")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting_multichoice[0].get("start_date", None)
        # print ("Start date: "+  start_date)
        end_date = voting_multichoice[0].get("end_date", None)
        # print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        # print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            # print("por aqui 42")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get("voter")
        vote = request.data.get("vote")

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post(
            "authentication", entry_point="/getuser/", json={"token": token}
        )

        voter_id = voter.get("id", None)
        if not voter_id or voter_id != uid:
            # print("por aqui 59")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get(
            "census/multichoice/{}".format(vid),
            params={"voter_id": uid},
            response=True,
        )
        if perms.status_code == 401:
            # print("por aqui 65")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")

        defs = {"a": a, "b": b}
        v, _ = VoteMultiChoice.objects.get_or_create(
            voting_multichoice_id=vid, voter_multichoice_id=uid
        )
        for option, value in vote.items():
            setattr(v, option, value)
            
        v.save()

        return Response({})
