from flask import Blueprint, render_template, request, redirect, url_for
from modelos.ofertas_modelo import agregar_oferta, obtener_ofertas
from servicio.upload_image import subir_imagen
from config.firebase_config import db

ofertas_bp = Blueprint('ofertas', __name__, template_folder='../vistas/Pantallas/Ofertas')

# Listar todas las ofertas
@ofertas_bp.route('/ofertas')
def listar_ofertas():
    productos = obtener_ofertas()
    for p in productos:
        print(f"Producto: {p.get('titulo')}, Imagen: {p.get('imagen')}")
    return render_template('Ofertas.html', productos=productos)


# Crear-Oferta todas las ofertas
@ofertas_bp.route('/crear-oferta', methods=['POST'])
def crear_oferta():
    try:
        data = dict(request.form)
        data["nuevo"] = True if data.get("nuevo") == "on" else False

        # Subir imagen
        if "imagen" in request.files and request.files["imagen"].filename != "":
            imagen = request.files["imagen"]
            print(f"Subiendo imagen: {imagen.filename}")
            data["imagen"] = subir_imagen(bucket_name="file", file_obj=imagen)
        else:
            data["imagen"] = ""

        # Guardar en Firebase
        agregar_oferta(data)
        print("Oferta creada exitosamente:", data)

    except Exception as e:
        print("Error creando oferta:", e)
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('ofertas.listar_ofertas'))



# Editar oferta
@ofertas_bp.route('/editar-oferta/<string:id>', methods=['POST'])
def editar_oferta(id):
    try:
        data = dict(request.form)

        # Subir nueva imagen si se proporciona
        if "imagen" in request.files and request.files["imagen"].filename != "":
            imagen = request.files["imagen"]
            data["imagen"] = subir_imagen("file", imagen)

        # Actualizar oferta en Firebase
        db.collection("oferta").document(id).update(data)
        print("Oferta actualizada:", data)

    except Exception as e:
        print("Error al editar oferta:", e)
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('ofertas.listar_ofertas'))

# Borrar oferta
@ofertas_bp.route('/borrar-oferta/<string:id>', methods=['POST'])
def borrar_oferta(id):
    try:
        db.collection("oferta").document(id).delete()
        print("Oferta borrada:", id)
    except Exception as e:
        print("Error al borrar oferta:", e)

    return redirect(url_for('ofertas.listar_ofertas'))
