from config.firebase_config import db

def agregar_oferta(formulario):
    """
    Guarda una oferta en Firebase.
    """
    try:
        nueva_oferta = {
            "titulo": formulario.get('titulo'),
            "tipoCafe": formulario.get('tipoCafe'),
            "variedad": formulario.get('variedad'),
            "clima": formulario.get('clima'),
            "fechaCosecha": formulario.get('fechaCosecha'),
            "altura": formulario.get('altura'),
            "cantidadProduccion": formulario.get('cantidadProduccion'),
            "estadoGrano": formulario.get('estadoGrano'),
            "procesoCorte": formulario.get('procesoCorte'),
            "ofertaLibra": formulario.get('ofertaLibra'),
            "imagen": formulario.get('imagen', ""),
            "lugarSeleccionado": formulario.get('lugarSeleccionado'),
            "userId": formulario.get('userId'),
            "nuevo": formulario.get('nuevo', False)
        }
        print("Oferta a guardar:", nueva_oferta)
        db.collection("oferta").add(nueva_oferta)
    except Exception as e:
        print("Error al agregar oferta:", e)
        import traceback
        print(traceback.format_exc())

def obtener_ofertas():
    try:
        productos = []
        docs = db.collection("oferta").stream()
        for doc in docs:
            producto = doc.to_dict()
            producto["id"] = doc.id
            productos.append(producto)
        print(f"Obtenidas {len(productos)} ofertas")
        return productos
    except Exception as e:
        print("Error al obtener ofertas:", e)
        return []
