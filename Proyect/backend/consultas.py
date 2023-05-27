import mysql.connector
import json
import random

# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bodegas_alianza_bda"
)

def TotalVentasAnuales():
    cursor = conexion.cursor()
    cursor.execute("""SELECT YEAR(f.fecha) AS fecha, ROUND(SUM(v.importe), 2) AS total
                        FROM ventas AS v
                        INNER JOIN facturas AS f ON v.num_factura = f.num_factura
                        GROUP BY YEAR(f.fecha)
                        ORDER BY fecha; """)
    resultado_raw = cursor.fetchall()
    cursor.close()

    anios = []
    for fila in resultado_raw:
        anios.append({"year": fila[0], "total": fila[1]})

    resultado = {"VentasTotales": anios}

    return resultado

def TotalVentasMensuales():
    cursor = conexion.cursor()
    cursor.execute("""SELECT YEAR(facturas.fecha) AS año, MONTHNAME(facturas.fecha) AS mes, ROUND(SUM(ventas.importe),2) AS total
                        FROM facturas, ventas
                        WHERE facturas.num_factura = ventas.num_factura
                        GROUP BY YEAR(facturas.fecha), MONTHNAME(facturas.fecha)
                        ORDER BY YEAR(facturas.fecha), MONTH(facturas.fecha);
                        """)
    ventas = cursor.fetchall()
    cursor.close()


    diccionario = {}
    for venta in ventas:
        if venta[0] not in diccionario:
            diccionario[venta[0]] = []
            diccionario[venta[0]].append({"month": venta[1], "total": venta[2]})
        else:
            diccionario[venta[0]].append({"month": venta[1], "total": venta[2]})

        
    resultado = {"VentasMensuales": diccionario}

    return resultado



def TodosLosProductos():
    cursor = conexion.cursor()
    consulta = """ SELECT YEAR(facturas.fecha) AS año, articulos.descripcion AS producto,ROUND(SUM(ventas.importe),2) AS total
                        FROM facturas, ventas, articulos
                        WHERE facturas.num_factura = ventas.num_factura
                        AND ventas.id_articulo = articulos.id_articulo
                        GROUP BY YEAR(facturas.fecha), articulos.descripcion
                        ORDER BY articulos.descripcion, YEAR(facturas.fecha);"""
    cursor.execute(consulta)
    productos = cursor.fetchall()
    cursor.close()

    lista1 = []
    lista2 = []
    lista3 = []
    for producto in productos:
        if producto[0] == 2020:
            lista1.append({"nombre": producto[1], "unidades_vendidas": producto[2]})
        elif producto[0] == 2021:
            lista2.append({"nombre": producto[1], "unidades_vendidas": producto[2]})
        elif producto[0] == 2022:
            lista3.append({"nombre": producto[1], "unidades_vendidas": producto[2]})

    dic2020 = {"year": "2020", "producto": lista1}
    dic2021 = {"year": "2021", "producto": lista2}
    dic2022 = {"year": "2022", "producto": lista3}

    resultado = {"ventasTotales": [dic2020, dic2021, dic2022]}
    return resultado
                
def Top10Productos():
    cursor = conexion.cursor()
    consulta = """ SELECT año, producto, total
                        FROM (
                            SELECT YEAR(facturas.fecha) AS año,
                                articulos.descripcion AS producto,
                                ROUND(SUM(ventas.importe),2) AS total,
                                ROW_NUMBER() OVER (PARTITION BY YEAR(facturas.fecha) ORDER BY SUM(ventas.importe) DESC) AS rn
                            FROM facturas
                            JOIN ventas ON facturas.num_factura = ventas.num_factura
                            JOIN articulos ON ventas.id_articulo = articulos.id_articulo
                            GROUP BY YEAR(facturas.fecha), articulos.descripcion
                        ) subquery
                        WHERE rn <= 10
                        ORDER BY año, total DESC;"""
    cursor.execute(consulta)
    productos = cursor.fetchall()
    cursor.close()

    lista1 = []
    lista2 = []
    lista3 = []
    for producto in productos:
        if producto[0] == 2020:
            lista1.append({"nombre": producto[1], "unidades_vendidas": producto[2]})
        elif producto[0] == 2021:
            lista2.append({"nombre": producto[1], "unidades_vendidas": producto[2]})
        elif producto[0] == 2022:
            lista3.append({"nombre": producto[1], "unidades_vendidas": producto[2]})

    dic2020 = {"year": "2020", "producto": lista1}
    dic2021 = {"year": "2021", "producto": lista2}
    dic2022 = {"year": "2022", "producto": lista3}

    resultado = {"ventasTotales": [dic2020, dic2021, dic2022]}
    return resultado


def codigosPostales():
    cursor = conexion.cursor()
    consulta = """ SELECT año, codigo_postal, vendido
                        FROM (
                            SELECT YEAR(facturas.fecha) as año,  facturas.codigo_postal AS codigo_postal, ROUND(SUM(ventas.importe),2) AS vendido
                            FROM ventas, facturas
                            WHERE ventas.num_factura = facturas.num_factura
                            AND YEAR(facturas.fecha) = "2020"
                            GROUP BY codigo_postal 
                            ORDER BY vendido DESC 
                            LIMIT 10
                        ) AS veinte
                        UNION
                        SELECT año, codigo_postal, vendido
                        FROM (
                            SELECT YEAR(facturas.fecha) as año,  facturas.codigo_postal AS codigo_postal, ROUND(SUM(ventas.importe),2) AS vendido
                            FROM ventas, facturas
                            WHERE ventas.num_factura = facturas.num_factura
                            AND YEAR(facturas.fecha) = "2021"
                            GROUP BY codigo_postal 
                            ORDER BY vendido DESC 
                            LIMIT 10
                        ) AS veintiuno
                        UNION
                        SELECT año, codigo_postal, vendido
                        FROM (
                            SELECT YEAR(facturas.fecha) as año,  facturas.codigo_postal AS codigo_postal, ROUND(SUM(ventas.importe),2) AS vendido
                            FROM ventas, facturas
                            WHERE ventas.num_factura = facturas.num_factura
                            AND YEAR(facturas.fecha) = "2022"
                            GROUP BY codigo_postal 
                            ORDER BY vendido DESC 
                            LIMIT 10
                        ) AS veintidos;"""
    cursor.execute(consulta)
    productos = cursor.fetchall()
    cursor.close()

    lista1 = []
    lista2 = []
    lista3 = []
    for producto in productos:
        if producto[0] == 2020:
            lista1.append({"CP": producto[1], "unidades_vendidas": producto[2]})
        elif producto[0] == 2021:
            lista2.append({"CP": producto[1], "unidades_vendidas": producto[2]})
        elif producto[0] == 2022:
            lista3.append({"CP": producto[1], "unidades_vendidas": producto[2]})

    dic2020 = {"year": "2020", "producto": lista1}
    dic2021 = {"year": "2021", "producto": lista2}
    dic2022 = {"year": "2022", "producto": lista3}

    resultado = {"ventasTotales": [dic2020, dic2021, dic2022]}
    return resultado


