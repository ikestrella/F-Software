from datetime import datetime
import os
from model.db import mysql  # Importa la instancia compartida



def get_productos_by_id(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchall()
    conn.commit()
    return producto


def delete_producto(id, carpeta):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT imagen FROM productos WHERE id=%s", (id,))
    fila = cursor.fetchall()
    os.remove(os.path.join(carpeta, fila[0][0]))

    cursor.execute("DELETE FROM productos WHERE id=%s;", (id,))
    conn.commit()

def update_producto(id, nombre, precio, foto, carpeta):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if foto.filename != '':
        nuevo_nombre_foto = tiempo + foto.filename
        foto.save(os.path.join(carpeta, nuevo_nombre_foto))

        cursor.execute("SELECT imagen FROM productos WHERE id=%s", (id,))
        fila = cursor.fetchall()
        os.remove(os.path.join(carpeta, fila[0][0]))

        cursor.execute("UPDATE productos SET imagen=%s WHERE id=%s", (nuevo_nombre_foto, id))
        conn.commit()

    cursor.execute("UPDATE productos SET nombre=%s, precio=%s WHERE id=%s;", (nombre, precio, id))
    conn.commit()

def create_producto(nombre, precio, foto, carpeta):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if foto.filename != '':
        nuevo_nombre_foto = tiempo + foto.filename
        foto.save(os.path.join(carpeta, nuevo_nombre_foto))

    cursor.execute("INSERT INTO `productos` (`nombre`, `precio`, `imagen`) VALUES (%s, %s, %s);", (nombre, precio, nuevo_nombre_foto))
    conn.commit()

    
def get_all_productos():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()
    conn.commit()
    return productos

