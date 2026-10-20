
import re

def normalizar_nit(texto):
    numeros = re.sub(r"\D", "", texto)

    if len(numeros) == 10:
        numeros = numeros[:9]

    if len(numeros) != 9:
        raise ValueError("NIT inválido")

    return numeros


def normalizar_factura(texto):
    texto = texto.upper().strip()
    texto = re.sub(r"[^A-Z0-9]", "", texto)
    texto = re.sub(r"^([A-Z]+)0+", r"\1", texto)

    if not texto or not re.search(r"\d", texto):
        raise ValueError("Factura inválida")

    return texto

###CASOS DE PRUEBA

# PRUEBAS VÁLIDAS
assert normalizar_nit("900.123.456-7") == "900123456"
assert normalizar_nit(" 900123456 ") == "900123456"
assert normalizar_nit("NIT 900 123 456") == "900123456"

assert normalizar_factura("FE-00123") == "FE123"
assert normalizar_factura("fe 123") == "FE123"
assert normalizar_factura("FE0123") == "FE123"


# PRUEBAS INVÁLIDAS
def probar_invalido(funcion, texto):
    try:
        funcion(texto)
    except ValueError:
        return

    raise AssertionError(f"Debía rechazar: {texto!r}")


probar_invalido(normalizar_nit, "")
probar_invalido(normalizar_nit, "ABC")
probar_invalido(normalizar_factura, "")
probar_invalido(normalizar_factura, "ABC")

print("Todas las pruebas pasaron correctamente")


"""
preguntaría si el último dígito corresponde al dígito de verificación,
porque quitarlo automáticamente podría alterar un identificador válido.
"""

"""
no asumiría que es la misma que FE123. Preguntaría si el sistema considera
que el prefijo FE puede omitirse, porque normalizar no debe cambiar el significado del dato.
"""

