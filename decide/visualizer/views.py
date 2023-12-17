import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.db.models import Count

from base import mods
from census.models import Census, CensusByPreference, CensusYesNo, CensusMultiChoice


class VisualizerView(TemplateView):
    template_name = "visualizer/visualizer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get("voting_id", 0)

        try:
            # Obtener la información de la votación
            r = mods.get("voting", params={"id": vid})
            context["voting"] = json.dumps(r[0])

            # Contar el censo para la votación específica
            voters_count = Census.objects.filter(voting_id=vid).aggregate(
                total=Count("voter_id", distinct=True)
            )["total"]
            voters_count = voters_count if voters_count else 0
            context["voters_count"] = voters_count

        except Exception as e:
            print(f"Error: {e}")
            raise Http404

        return context


class VisualizerViewYesNo(TemplateView):
    template_name = "visualizer/visualizerYesNo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get("voting_yesno_id", 0)

        try:
            # Obtener la información de la votación
            r = mods.get("voting/yesno", params={"id": vid})
            context["voting"] = json.dumps(r[0])

            # Contar el censo para la votación específica
            voters_count = CensusYesNo.objects.filter(voting_id=vid).aggregate(
                total=Count("voter_id", distinct=True)
            )["total"]
            voters_count = voters_count if voters_count else 0
            context["voters_count"] = voters_count

        except Exception as e:
            print(f"Error: {e}")
            raise Http404

        return context


class VisualizerViewPreference(TemplateView):
    template_name = "visualizer/visualizer_preference.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get("voting_preference_id", 0)

        try:
            # Obtener la información de la votación
            r = mods.get("voting/preference", params={"id": vid})
            context["voting"] = json.dumps(r[0])

            # Contar el censo para la votación específica
            voters_count = CensusByPreference.objects.filter(voting_id=vid).aggregate(
                total=Count("voter_id", distinct=True)
            )["total"]
            voters_count = voters_count if voters_count else 0
            context["voters_count"] = voters_count

        except Exception as e:
            print(f"Error: {e}")
            raise Http404

        return context

class VisualizerViewMultiChoice(TemplateView):
    template_name = "visualizer/visualizerMultiChoice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get("voting_multichoice_id", 0)

        try:
            # Obtener la información de la votación
            r = mods.get("voting/multichoice", params={"id": vid})
            context["voting"] = json.dumps(r[0])

            # Contar el censo para la votación específica
            voters_count = CensusMultiChoice.objects.filter(voting_id=vid).aggregate(
                total=Count("voter_id", distinct=True)
            )["total"]
            voters_count = voters_count if voters_count else 0
            context["voters_count"] = voters_count

        except Exception as e:
            print(f"Error: {e}")
            raise Http404

        return context