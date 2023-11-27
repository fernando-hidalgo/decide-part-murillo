from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting
from .models import QuestionYesNo
from .models import VotingYesNo
from .filters import StartedFilter

from django.http import HttpResponse
import io
import json


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get("auth-token", "")
        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class QuestionYesNoAdmin(admin.ModelAdmin):
    list_display = ("desc", "optionYes", "optionNo")
    readonly_fields = ("optionYes", "optionNo")
    list_filter = (StartedFilter,)
    search_fields = ("desc",)


class VotingAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    readonly_fields = ("start_date", "end_date", "pub_key", "tally", "postproc")
    date_hierarchy = "start_date"
    list_filter = (StartedFilter,)
    search_fields = ("name",)

    def start(modeladmin, request, queryset):
        for v in queryset.all():
            v.create_pubkey()
            v.start_date = timezone.now()
            v.save()

    def stop(ModelAdmin, request, queryset):
        for v in queryset.all():
            v.end_date = timezone.now()
            v.save()

    def tally(ModelAdmin, request, queryset):
        for v in queryset.filter(end_date__lt=timezone.now()):
            token = request.session.get("auth-token", "")
            v.tally_votes(token)

    def voting_result_data(modeladmin, request, queryset):
        json_buffer = io.StringIO()
        json_objects = []

        for voting in queryset:
            data = {
                "Voting ID": voting.id,
                "Voting Name": voting.name,
                "Tally": voting.tally,
                "Postproc": voting.postproc,
            }

            json_objects.append(data)

        data_json = json.dumps(json_objects, indent=2)

        json_buffer.write(data_json)

        response = HttpResponse(json_buffer.getvalue(), content_type="text/plain")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="voting_result_data.json"'

        return response

    voting_result_data.short_description = "Exportar resultados"

    actions = [start, stop, tally, voting_result_data]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionYesNo, QuestionYesNoAdmin)
admin.site.register(VotingYesNo, VotingAdmin)
