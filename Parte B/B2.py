from decimal import Decimal

def armar_reporte(filas):
    proveedores = {}

    for fila in filas:
        nit = fila["nit"]
        monto = Decimal(str(fila["total_pesos"]))

        if nit not in proveedores:
            proveedores[nit] = {
                "nit": nit,
                "proveedor": fila["proveedor"],
                "total": Decimal("0"),
                "meses": []
            }

        p = proveedores[nit]

        p["total"] += monto

        p["meses"].append({
            "mes": fila["mes"],
            "documentos": fila["documentos"],
            "total_pesos": format(monto, ".2f")
        })

    # Ordenar meses del más antiguo al más reciente
    for p in proveedores.values():
        p["meses"].sort(key=lambda m: m["mes"])

    # Ordenar proveedores por total, de mayor a menor
    ordenados = sorted(
        proveedores.values(),
        key=lambda p: p["total"],
        reverse=True
    )

    # Crear la salida final
    return [
        {
            "nit": p["nit"],
            "proveedor": p["proveedor"],
            "total_pesos": format(p["total"], ".2f"),
            "meses": p["meses"]
        }
        for p in ordenados
    ]

"""
Usaría Decimal en Python para sumar los montos,
porque permite trabajar con valores decimales de forma precisa.
No usaría float porque puede generar pequeños errores de precisión en operaciones con dinero.
"""

"""
Lo mostraría con su valor negativo, sin cambiarlo a cero ni eliminarlo del reporte. 
Le preguntaría al usuario si desea mostrar estos proveedores y si el saldo negativo 
debe interpretarse como un saldo a favor.
"""