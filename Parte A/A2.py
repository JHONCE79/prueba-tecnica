"""
PROBLEMAS
#1

for c in compras:
    lineas = db.query(
        "SELECT * FROM compras_productos WHERE compra_id = ?",
        [c.id]
    )

Hay un problema de rendimiento porque se hace una consulta
para obtener las compras y luego otra consulta por cada compra 
para buscar sus productos. Esto genera demasiadas consultas y hace que el programa sea lento.
"""
########################
"""
#2
total = 0.0
total = total + l.cantidad * l.valor

Al ser numeros tipo float puede producir pequeños errores de precision, es mejor usar decimal
"""
#########################
"""
#3
compras = db.query(
    "SELECT * FROM compras WHERE estado <> 'ANULADO'"
)

Hay un problema de memoria y rendimiento porque se traen todas las compras
y todas sus columnas, aunque no se necesitan todos esos datos.
"""
#############################
##### CODIGO CORREGIDO ######
#############################



import psycopg

try:
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="prueba_tecnica",
        user="postgres",
        password="1234"
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.id,
                    c.consecutivo,
                    c.subtotal,
                    COALESCE(SUM(cp.cantidad * cp.valor), 0) AS total
                FROM compras c
                LEFT JOIN compras_productos cp
                    ON cp.compra_id = c.id
                WHERE c.estado <> 'ANULADO'
                GROUP BY c.id, c.consecutivo, c.subtotal
                HAVING ABS(
                    COALESCE(SUM(cp.cantidad * cp.valor), 0)
                    - c.subtotal
                ) > 1
                ORDER BY c.id
            """)

            while True:
                filas = cur.fetchmany(1000)

                if not filas:
                    break

                for c in filas:
                    id_compra, consecutivo, subtotal, total = c
                    print(
                        "Compra inconsistente:",
                        consecutivo,
                        "Total de líneas:", total,
                        "Subtotal:", subtotal
                    )

except Exception as e:
    print("Error:", e)

