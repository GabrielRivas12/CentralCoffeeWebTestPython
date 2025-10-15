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
            "nuevo": data.get('nuevo', False)
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
                productos.append(producto)
            print(f"Obtenidas {len(productos)} ofertas")
            return productos
        except Exception as e:
            print("Error al obtener ofertas:", e)
            return []

    def obtener_uno(self, id):
        return super().obtener_uno(id)
    
    def actualizar(self, id, data):
        
        try:
            db.collection("oferta").document(id).update(data)
            print("Oferta actualizada:", data)
        except Exception as e:
            print("Error al actualizar el documento: " + e)
    
    def eliminar(self, id):
        db.collection("oferta").document(id).delete()
        print("Oferta borrada:", id)
    
    def guardar_imagen(self, bucket_name, file_obj, file_key = None):
        try:
            print(f"Iniciando subida de imagen: {file_obj.filename}")

            # Extensión del archivo
            ext = file_obj.filename.split('.')[-1] if '.' in file_obj.filename else 'jpg'

            # Generar nombre único
            if not file_key:
                file_key = f"{uuid.uuid4()}.{ext}"   # aqui es donde la imagen se guarda en el supabase 
            else:                                    # en la carpeta file
                file_key = f"{file_key}"

            # Leer contenido
            file_obj.seek(0)
            contenido = file_obj.read()

        # ✅ CORREGIDO: usar 'true' como string en lugar de True booleano
            res = supabase.storage.from_(bucket_name).upload(
                file_key,
                contenido,
                {
                    "content-type": file_obj.content_type,
                    "upsert": "true"  # ← AQUÍ ESTÁ LA CORRECCIÓN
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