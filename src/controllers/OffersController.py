from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from ..services.OffersRepositoryImpl import OffersRepositoryImpl
from ..services.UserRepository import UserRepositoryImpl
from ..config.FirebaseConfig import db

repository = OffersRepositoryImpl()
usrRepository = UserRepositoryImpl()

subDir = 'screens/Ofertas'

ofertas_bp = Blueprint('ofertas', __name__)

@ofertas_bp.route('/ofertas', methods=['GET'])
def listar_ofertas():
    if request.method != 'GET':
        return "Método no permitido", 405
    else:
        user = usrRepository.get_user_by_uid(session.get('user_uid'))
        productos = repository.obtener_todos()
        lugares_list = repository.obtener_lugares()
        
        lugares_dict = {lugar['id']: lugar for lugar in lugares_list}

        print(user)
        for p in productos:
            print(f"Producto: {p.get('titulo')}, Estado: {p.get('estado')}")
        
        for lugar_id, lugar in lugares_dict.items():
            print(f"Lugar ID: {lugar_id}, Nombre: {lugar.get('nombre')}")
            
        return render_template(subDir + '/Ofertas.html', 
                             productos=productos, 
                             user=user, 
                             lugares=lugares_list,
                             lugares_dict=lugares_dict)

@ofertas_bp.route('/crear-oferta', methods=['POST'])
def crear_oferta():
    try:
        data = dict(request.form)
        
        data["userId"] = session.get('user_uid')
        
        if "imagen" in request.files and request.files["imagen"].filename != "":
            imagen = request.files["imagen"]
            print(f"Subiendo imagen: {imagen.filename}")
            data["imagen"] = repository.guardar_imagen(bucket_name='file', file_obj=imagen)
        else:
            flash('La imagen es requerida', 'error')
            return redirect(url_for('ofertas.listar_ofertas'))
            
        success = repository.crear(data=data)
        
        if success:
            flash('Oferta creada exitosamente', 'success')
        else:
            flash('Error al crear la oferta', 'error')

    except Exception as e:
        print("Error obteniendo los datos del formulario:", e)
        flash('Error al crear la oferta', 'error')
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('ofertas.listar_ofertas'))

@ofertas_bp.route('/editar-oferta/<string:id>', methods=['POST'])
def editar_oferta(id):
    try:
        oferta_actual = repository.obtener_por_id(id)
        if not oferta_actual:
            flash('Oferta no encontrada', 'error')
            return redirect(url_for('ofertas.listar_ofertas'))
        
        user_role = session.get('user_role')
        user_uid = session.get('user_uid')
        
        if user_role != 'Administrador' and oferta_actual.get('userId') != user_uid:
            flash('No tienes permisos para editar esta oferta', 'error')
            return redirect(url_for('ofertas.listar_ofertas'))

        data = dict(request.form)
        data["nuevo"] = True if data.get("nuevo") == "on" else False

        if "imagen" in request.files and request.files["imagen"].filename != "":
            imagen = request.files["imagen"]
            data["imagen"] = repository.guardar_imagen(bucket_name='file', file_obj=imagen)

        repository.actualizar(id=id, data=data)
        flash('Oferta actualizada exitosamente', 'success')

    except Exception as e:
        print("Error al obtener los datos del formulario:", e)
        flash('Error al actualizar la oferta', 'error')
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('ofertas.listar_ofertas'))

@ofertas_bp.route('/borrar-oferta/<string:id>', methods=['POST'])
def borrar_oferta(id):
    try:
        oferta_actual = repository.obtener_por_id(id)
        if not oferta_actual:
            flash('Oferta no encontrada', 'error')
            return redirect(url_for('ofertas.listar_ofertas'))
        
        user_role = session.get('user_role')
        user_uid = session.get('user_uid')
        
        if user_role != 'Administrador' and oferta_actual.get('userId') != user_uid:
            flash('No tienes permisos para eliminar esta oferta', 'error')
            return redirect(url_for('ofertas.listar_ofertas'))

        repository.eliminar(id=id)
        flash('Oferta eliminada exitosamente', 'success')
        
    except Exception as e:
        print("Error al borrar oferta:", e)
        flash('Error al eliminar la oferta', 'error')

    return redirect(url_for('ofertas.listar_ofertas'))

@ofertas_bp.route('/cambiar-estado-oferta/<string:id>', methods=['POST'])
def cambiar_estado_oferta(id):
    try:
        if session.get('user_role') != 'Administrador':
            flash('No tienes permisos para cambiar el estado de ofertas', 'error')
            return redirect(url_for('ofertas.listar_ofertas'))

        oferta_actual = repository.obtener_por_id(id)
        if oferta_actual:
            estado_actual = oferta_actual.get('estado', 'Activo')
            nuevo_estado = "Inactivo" if estado_actual == "Activo" else "Activo"
            data = {"estado": nuevo_estado}
            repository.actualizar(id=id, data=data)
            flash(f'Estado cambiado a {nuevo_estado}', 'success')
            print(f"Estado de oferta {id} cambiado de '{estado_actual}' a: '{nuevo_estado}'")
        else:
            flash('Oferta no encontrada', 'error')
            print(f"Oferta con id {id} no encontrada")
            
    except Exception as e:
        print("Error al cambiar estado de oferta:", e)
        flash('Error al cambiar el estado de la oferta', 'error')
        import traceback
        print(traceback.format_exc())

    return redirect(url_for('ofertas.listar_ofertas'))