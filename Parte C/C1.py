
import csv
import re
from decimal import Decimal
from datetime import date


def convertir_monto(texto):
    return Decimal(texto.replace(".", "").replace(",", "."))


def conciliar(egresos, archivo):
    with open(archivo, encoding="utf-8") as f:
        banco = list(csv.DictReader(f, delimiter=";"))

    usados = set()
    resultado = []

    for m in banco:
        fecha_banco = date.fromisoformat(m["fecha"])
        valor_banco = convertir_monto(m["debito"])
        descripcion = m["descripcion"]
        candidatos = []

        for i, e in enumerate(egresos):
            dias = (fecha_banco - e["fecha"]).days

            if (i not in usados
                and valor_banco == e["valor"]
                and 0 <= dias <= 3):

                patron = r"EG[\s-]*" + str(e["consecutivo"]) + r"\b"

                if re.search(patron, descripcion, re.I):
                    candidatos = [i]
                    break

                if e["nit"] in descripcion:
                    candidatos.append(i)

        if len(candidatos) == 1:
            i = candidatos[0]
            usados.add(i)

            patron = r"EG[\s-]*" + str(
                egresos[i]["consecutivo"]
            ) + r"\b"

            tipo = (
                "fuerte"
                if re.search(patron, descripcion, re.I)
                else "debil"
            )

            resultado.append((m, egresos[i], tipo))
        else:
            resultado.append((m, None, "solo en banco"))

    for i, e in enumerate(egresos):
        if i not in usados:
            resultado.append((None, e, "solo en ERP"))

    return resultado
