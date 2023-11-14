from rest_framework.views import APIView
from rest_framework.response import Response
import json


class PostProcView(APIView):
    def apply_identity(self, options):
        out = []

        for opt in options:
            out.append(
                {
                    **opt,
                    "postproc": opt["votes"],
                }
            )

        out.sort(key=lambda x: -x["postproc"])

        return Response(out)

    def apply_hont(self, options, escaños):

        votos = [opt["votes"] for opt in options]
        total_escaños = escaños  # Obtener el número total de escaños o 0 si no existe

        resultados = (
            []
        )  # Lista para almacenar el número de escaños asignados y otros parámetros a cada lista

        # Inicializar el número de escaños asignados a cada lista en 0
        for opt in options:
            resultados.append({**opt, "seats": 0})

        # Verificar si se proporcionó el número total de escaños
        if total_escaños > 0:
            # Asignar escaños utilizando la ley D'Hondt
            for i in range(total_escaños):
                max_lista = max(votos)
                index_max = votos.index(max_lista)
                resultados[index_max]["seats"] += 1
                votos[index_max] = votos[index_max] / (
                    resultados[index_max]["seats"] + 1
                )

            # Ordenar los resultados por la cantidad de escaños asignados (en orden descendente)
            resultados.sort(key=lambda x: -x["seats"])

        return Response(resultados)

    def post(self, request):
        """
        * type: IDENTITY | EQUALITY | WEIGHT | HONT
        * options: [
           {
            option: str,
            number: int,
            votes: int,
            ...extraparams
           }
          ]
        """

        t = request.data.get("type", "IDENTITY")
        escaños = request.data.get("escaños", 10)
        opts = request.data.get("options", [])

        if t == "IDENTITY":
            return self.apply_identity(opts)
        if t == "HONT":
            return self.apply_hont(opts, escaños)

        return Response({})
