
import csv
import os
import psycopg

CSV = "compras.csv"
PROGRESO = "progreso_a1.txt"
LOTE = 1000

try:
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="prueba_tecnica",
        user="postgres",
        password="1234"
    ) as conn:

        # Si ya hay progreso, continuar
        if os.path.exists(PROGRESO):
            with open(PROGRESO) as f:
                ultimo_id = int(f.readline()) #ultima compra exportada correctamente
                id_maximo = int(f.readline()) # limite de id establedcido 
                posicion = int(f.readline()) #punto del csv donde termino

            if not os.path.exists(CSV):
                raise Exception("Falta el archivo CSV")

            modo = "r+"

        else:
            with conn.cursor() as cur:
                cur.execute("SELECT COALESCE(MAX(id), 0) FROM compras")
                id_maximo = cur.fetchone()[0]

            ultimo_id = 0
            posicion = 0
            modo = "w+"

        with open(CSV, modo, newline="", encoding="utf-8-sig") as f:

            if modo == "w+":
                csv.writer(f).writerow([
                    "consecutivo", "fecha", "nit",
                    "proveedor", "moneda", "neto",
                    "neto_pesos"
                ])
                f.flush()
                posicion = f.tell()

                with open(PROGRESO, "w") as p:
                    p.write(f"{ultimo_id}\n{id_maximo}\n{posicion}\n")

            else:
                f.seek(posicion)


            while True:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT c.id, c.consecutivo, c.fecha,
                               t.numeroidentificacion, t.nombrecompleto,
                               m.nombre, c.neto,
                               c.neto * CASE WHEN c.trm = 0
                                             THEN 1 ELSE c.trm END
                        FROM compras c
                        JOIN terceros t ON t.id = c.proveedor_id
                        JOIN monedas m ON m.id = c.moneda_id
                        JOIN documentos_compras dc
                            ON dc.id = c.documentocompra_id
                        WHERE dc.codigo = 'CP'
                          AND c.estado <> 'ANULADA'
                          AND c.id > %s AND c.id <= %s
                        ORDER BY c.id
                        LIMIT %s
                    """, (ultimo_id, id_maximo, LOTE))

                    filas = cur.fetchall()

                if not filas:
                    break

                escritor = csv.writer(f)

                for fila in filas:
                    escritor.writerow(fila[1:])
                    ultimo_id = fila[0]

                f.flush()
                os.fsync(f.fileno())
                posicion = f.tell()

                with open(PROGRESO, "w") as p:
                    p.write(f"{ultimo_id}\n{id_maximo}\n{posicion}\n")

                print("Último ID exportado:", ultimo_id)

    print("Exportación terminada.")

except Exception as e:
    print("Error:", e)


"""
No usaria OFFSET, porque con muchos registros se vuelve lento. 
Usaría el ID para continuar desde donde quedé.
"""

"""
En SQL, porque puedo calcularlo directamente con CASE y Python 
solo guarda los resultados en el CSV.
"""