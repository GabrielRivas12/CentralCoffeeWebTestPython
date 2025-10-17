from flask import Blueprint, render_template, request, redirect, session, url_for
from ..services.OffersRepositoryImpl import OffersRepositoryImpl
from ..services.UserRepository import UserRepositoryImpl
from ..config.FirebaseConfig import db

#creación de la instancia del repositorio
repository = OffersRepositoryImpl()

usrRepository = UserRepositoryImpl()

subDir = 'screens/Ofertas'

ofertas_bp = Blueprint('ofertas', __name__)

# Listar todas las ofertas
@ofertas_bp.route('/ofertas', methods=['GET'])
def listar_ofertas():
    if request.method != 'GET':
        return "Método no permitido", 405
    else:
        user = usrRepository.get_user_by_uid(session.get('user').get('uid'))
        productos = repository.obtener_todos()

        print(user)
        # linea de debug
        for p in productos:
            print(f"Producto: {p.get('titulo')}, Imagen: {p.get('imagen')}")
        return render_template(subDir + '/Ofertas.html', productos=productos, user=user)


# Crear-Oferta todas las ofertas
@ofertas_bp.route('/crear-oferta', methods=['POST'])
def crear_oferta():
    try:
        data = dict(request.form)
        data["nuevo"] = True if data.get("nuevo") == "on" else False

        # Subir imagen
        if "imagen" in request.files and request.files["imagen"].filename != "":
            imagen = request.files["imagen"]
            # linea de debug
            print(f"Subiendo imagen: {imagen.filename}")
            data["imagen"] = repository.guardar_imagen(bucket_name='file', file_obj=imagen)
        else:
            data["imagen"] = ""
            
        repository.crear(data=data)

    except Exception as e:
        print("Error obteniendo los datos del formulario:", e)
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
            data["imagen"] = repository.guardar_imagen(bucket_name='file', file_obj=imagen)

        repository.actualizar(id=id, data=data)

    except Exception as e:
        print("Error al obtener los datos del formulario:", e)
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('ofertas.listar_ofertas'))

# Borrar oferta
@ofertas_bp.route('/borrar-oferta/<string:id>', methods=['POST'])
def borrar_oferta(id):
    try:
        repository.eliminar(id= id)
    except Exception as e:
        print("Error al borrar oferta:", e)

    return redirect(url_for('ofertas.listar_ofertas'))
