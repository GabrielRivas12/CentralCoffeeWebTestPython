import uuid
from servicio.supabase_config import supabase

def subir_imagen(bucket_name: str, file_obj, file_key: str = None) -> str:
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