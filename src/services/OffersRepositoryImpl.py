from lib2to3.fixes.fix_filter import FixFilter
from .repository.IOffersRepository import IOffersRepository
from ..config.FirebaseConfig import db

import uuid
from ..config.SupabaseConfig import supabase

class OffersRepositoryImpl(IOffersRepository):
    
    def crear(self, data):
        try:
            nueva_oferta = {
            "titulo": data.get('titulo'),
            "tipoCafe": data.get('tipoCafe'),
            "variedad": data.get('variedad'),
            "clima": data.get('clima'),
            "fechaCosecha": data.get('fechaCosecha'),
            "altura": data.get('altura'),
            "cantidadProduccion": data.get('cantidadProduccion'),
            "estadoGrano": data.get('estadoGrano'),
            "procesoCorte": data.get('procesoCorte'),
            "ofertaLibra": data.get('ofertaLibra'),
            "imagen": data.get('imagen', ""),
            "lugarSeleccionado": data.get('lugarSeleccionado'),
            "userId": data.get('userId'),
            "estado": "Activo"
        }
            print("Oferta a guardar:", nueva_oferta)
            db.collection("oferta").add(nueva_oferta)
        except Exception as e:
            print("Error al agregar oferta:", e)
            import traceback
            print(traceback.format_exc())
            
    def obtener_todos(self):
        try:
            productos = []
            docs = db.collection("oferta").stream()
            for doc in docs:
                producto = doc.to_dict()
                producto["id"] = doc.id
                if 'estado' not in producto:
                    producto['estado'] = 'Activo'
                productos.append(producto)
            print(f"Obtenidas {len(productos)} ofertas")
            return productos
        except Exception as e:
            print("Error al obtener ofertas:", e)
            return []

    def obtener_uno(self, id):
        try:
            productos = []
            doc_ref = db.collection("oferta")
            query = (
                doc_ref.where("userId", "==", id).stream()
                )

            for doc in query:
                producto = doc.to_dict()
                producto['id'] = doc.id
                if 'estado' not in producto:
                    producto['estado'] = 'Activo'
                productos.append(producto)

            return productos
        except Exception as e:
            print("Error al obtener la oferta:", e)
            return None
    
    def obtener_por_id(self, id):
        """
        Obtiene una oferta específica por su ID de documento
        """
        try:
            doc_ref = db.collection("oferta").document(id)
            doc = doc_ref.get()
            if doc.exists:
                producto = doc.to_dict()
                producto["id"] = doc.id
                if 'estado' not in producto:
                    producto['estado'] = 'Activo'
                return producto
            else:
                print(f"Documento con id {id} no encontrado")
                return None
        except Exception as e:
            print("Error al obtener oferta por ID:", e)
            return None
    
    def actualizar(self, id, data):
        try:
            if 'nuevo' in data:
                data['nuevo']
                
            db.collection("oferta").document(id).update(data)
            print(f"Oferta {id} actualizada: {data}")
        except Exception as e:
            print("Error al actualizar el documento: " + str(e))
            import traceback
            print(traceback.format_exc())
    
    def eliminar(self, id):
        db.collection("oferta").document(id).delete()
        print("Oferta borrada:", id)
    
    def guardar_imagen(self, bucket_name, file_obj, file_key = None):
        try:
            print(f"Iniciando subida de imagen: {file_obj.filename}")

            # Extensión del archivo
            ext = file_obj.filename.split('.')[-1] if '.' in file_obj.filename else 'jpg'

            # Generar nombe
            if not file_key:
                file_key = f"{uuid.uuid4()}.{ext}"   # aqui es donde la imagen se guarda en el supabase 
            else:                                   
                file_key = f"{file_key}"

            # Leer contenido
            file_obj.seek(0)
            contenido = file_obj.read()

            res = supabase.storage.from_(bucket_name).upload(
                file_key,
                contenido,
                {
                    "content-type": file_obj.content_type,
                    "upsert": "true"  
                }
            )
            print("Respuesta Supabase:", res)

            # Obtener URL pública
            public_url = supabase.storage.from_(bucket_name).get_public_url(file_key)
            print("URL pública generada:", public_url)

            return str(public_url)

        except Exception as e:
            print("Error subiendo imagen:", e)
            import traceback
            print(traceback.format_exc())
            return ""
        
    def obtener_lugares(self):
        """
        Obtiene todos los lugares de la colección 'lugares'
        """
        try:
            lugares = []
            docs = db.collection("lugares").stream()
            for doc in docs:
                lugar = doc.to_dict()
                lugar["id"] = doc.id
                lugares.append(lugar)
            print(f"Obtenidos {len(lugares)} lugares")
            return lugares
        except Exception as e:
            print("Error al obtener lugares:", e)
            return []