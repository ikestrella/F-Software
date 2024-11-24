from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from model.obra import *
from model.producto import *
import os   
from model.db import init_app

app = Flask(__name__, template_folder='views')
app.secret_key = "Develoteca"

CARPETA = os.path.join('imagenes')
app.config['CARPETA'] = CARPETA

init_app(app)

@app.route('/imagenes/<nombreFoto>')
def imagenes(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.route('/')
def index():
    obras = get_all_obras()
    productos = get_all_productos()
    return render_template('vista/index.html', obras=obras, productos=productos)

@app.route('/destroy/<int:id>')
def destroy(id):
    delete_obra(id, app.config['CARPETA'])
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    obras = get_obras_by_id(id)
    return render_template('vista/edit.html', obras=obras)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtnombre']
    _descripcion = request.form['txtcorreo']
    _foto = request.files['txtfoto']
    id = request.form['txtID']
    
    update_obra(id, _nombre, _descripcion, _foto, app.config['CARPETA'])
    return redirect('/')

@app.route('/create')
def create():
    return render_template('vista/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtnombre']
    _descripcion = request.form['txtcorreo']
    _foto = request.files['txtfoto']

    if _nombre == '' or _descripcion == '' or _foto == '':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))

    create_obra(_nombre, _descripcion, _foto, app.config['CARPETA'])
    return redirect('/')

@app.route('/createP')
def createP():
    return render_template('vista/createP.html')

@app.route('/destroyP/<int:id>')
def destroyP(id):
    delete_producto(id, app.config['CARPETA'])
    return redirect('/')

@app.route('/editP/<int:id>')
def editP(id):
    productos = get_productos_by_id(id)
    return render_template('vista/editP.html', productos=productos)

@app.route('/updateP', methods=['POST'])
def updateP():
    _nombre = request.form['txtnombre']
    _precio = request.form['txtprecio']
    _foto = request.files['txtfoto']
    id = request.form['txtID']

    update_producto(id, _nombre, _precio, _foto, app.config['CARPETA'])
    return redirect('/')

@app.route('/storeP', methods=['POST'])
def storageP():
    _nombre = request.form['txtnombre']
    _precio = request.form['txtprecio']
    _foto = request.files['txtfoto']

    if _nombre == '' or _precio == '' or _foto == '':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createP'))

    create_producto(_nombre, _precio, _foto, app.config['CARPETA'])
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
