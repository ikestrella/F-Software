from flaskext.mysql import MySQL
from datetime import datetime
import os

mysql = MySQL()

def init_app(app):
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'portafolio'
    mysql.init_app(app)

def get_all_obras():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `obras`;")
    obras = cursor.fetchall()
    conn.commit()
    return obras

def get_all_productos():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()
    conn.commit()
    return productos

def get_obras_by_id(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM obras WHERE id=%s", (id,))
    obra = cursor.fetchall()
    conn.commit()
    return obra

def get_productos_by_id(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchall()
    conn.commit()
    return producto

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
