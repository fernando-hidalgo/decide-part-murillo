from django.contrib import admin

from .models import Census

from django.http import HttpResponse
from openpyxl import Workbook

from .models import Census  # Asegúrate de importar tu modelo correctamente


class CensusAdmin(admin.ModelAdmin):
    list_display = ("voting_id", "voter_id")
    list_filter = ("voting_id",)
    search_fields = ("voter_id",)

    actions = ["exportar_a_excel"]

    def exportar_a_excel(modeladmin, request, queryset):
        workbook = Workbook()
        sheet = workbook.active

        sheet.append(
            ["ID Votacion", "ID Votante"]
        )  # El append funciona en filas, de izquierda a derecha

        for elemento in queryset:
            sheet.append([elemento.voting_id, elemento.voter_id])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=exportacion_excel.xlsx"
        workbook.save(response)

        return response

    exportar_a_excel.short_description = "Exportar a Excel"


admin.site.register(Census, CensusAdmin)
