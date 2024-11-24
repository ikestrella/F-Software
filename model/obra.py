from datetime import datetime
import os
from model.db import mysql  # Importa la instancia compartida


def get_all_obras():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `obras`;")
    obras = cursor.fetchall()
    conn.commit()
    return obras



def get_obras_by_id(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM obras WHERE id=%s", (id,))
    obra = cursor.fetchall()
    conn.commit()
    return obra



def delete_obra(id, carpeta):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT imagen FROM obras WHERE id=%s", (id,))
    fila = cursor.fetchall()
    os.remove(os.path.join(carpeta, fila[0][0]))

    cursor.execute("DELETE FROM obras WHERE id=%s;", (id,))
    conn.commit()

def update_obra(id, nombre, descripcion, foto, carpeta):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if foto.filename != '':
        nuevo_nombre_foto = tiempo + foto.filename
        foto.save(os.path.join(carpeta, nuevo_nombre_foto))

        cursor.execute("SELECT imagen FROM obras WHERE id=%s", (id,))
        fila = cursor.fetchall()
        os.remove(os.path.join(carpeta, fila[0][0]))

        cursor.execute("UPDATE obras SET imagen=%s WHERE id=%s", (nuevo_nombre_foto, id))
        conn.commit()

    cursor.execute("UPDATE obras SET nombre=%s, descripcion=%s WHERE id=%s;", (nombre, descripcion, id))
    conn.commit()

def create_obra(nombre, descripcion, foto, carpeta):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if foto.filename != '':
        nuevo_nombre_foto = tiempo + foto.filename
        foto.save(os.path.join(carpeta, nuevo_nombre_foto))

    cursor.execute("INSERT INTO `obras` (`nombre`, `descripcion`, `imagen`) VALUES (%s, %s, %s);", (nombre, descripcion, nuevo_nombre_foto))
    conn.commit()
