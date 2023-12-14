from rest_framework import serializers
from .models import Census


class CensusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Census
        fields = [
            "voting_id",
            "voter_id",
        ]  # Asegúrate de que estos campos sean correctos
