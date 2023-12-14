from rest_framework.views import APIView
from rest_framework.response import Response


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

    def apply_hont(self, options, escaños, preference):

        votos = [opt["votes"] for opt in options]
        total_escaños = escaños
        resultados = []

        for opt in options:
            resultados.append({**opt, "seats": 0})

        if total_escaños > 0:

            while total_escaños > 0:
                if preference:
                    max_lista = min(votos)
                else:
                    max_lista = max(votos)
                index_max = votos.index(max_lista)
                resultados[index_max]["seats"] += 1
                if preference:
                    votos[index_max] = options[index_max]["votes"] * (
                        resultados[index_max]["seats"] + 1
                    )
                else:
                    votos[index_max] = options[index_max]["votes"] / (
                        resultados[index_max]["seats"] + 1
                    )
                total_escaños -= 1

            resultados.sort(key=lambda x: -x["seats"])

        return Response(resultados)

    def apply_lague(self, options, escaños, preference):
        votos = [opt["votes"] for opt in options]
        total_escaños = escaños
        resultados = []

        for opt in options:
            resultados.append({**opt, "seats": 0})

        if total_escaños > 0:
            while total_escaños > 0:
                if preference:
                    max_lista = min(votos)
                else:
                    max_lista = max(votos)
                index_max = votos.index(max_lista)
                resultados[index_max]["seats"] += 1
                if preference:
                    votos[index_max] = votos[index_max] * (
                        2 * resultados[index_max]["seats"] + 1
                    )
                else:
                    votos[index_max] = votos[index_max] / (
                        2 * resultados[index_max]["seats"] + 1
                    )
                total_escaños -= 1

            resultados.sort(key=lambda x: -x["seats"])

        return Response(resultados)

    def post(self, request):
        """
        * type: IDENTITY | EQUALITY | WEIGHT | HONT | LAGUE
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
        preference = request.data.get("preference", False)

        if t == "IDENTITY":
            return self.apply_identity(opts)
        if t == "HONT":
            return self.apply_hont(opts, escaños, preference)
        elif t == "LAGUE":
            return self.apply_lague(opts, escaños, preference)

        return Response({})
