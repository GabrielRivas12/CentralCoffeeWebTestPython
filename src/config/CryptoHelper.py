import base64
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# La clave secreta proporcionada por el usuario
SECRET_KEY = "tu_clave_secreta_32_caracteres!!!".encode('utf-8')

def evp_bytes_to_key(password, salt, key_len, iv_len):
    """
    Deriva una clave y un IV a partir de una contraseña y una sal,
    replicando el comportamiento de EVP_BytesToKey de OpenSSL (usando MD5).
    """
    dtot = b''
    d = b''
    while len(dtot) < key_len + iv_len:
        d = md5(d + password + salt).digest()
        dtot += d
    return dtot[:key_len], dtot[key_len:key_len+iv_len]

class EncryptionManager:
    def encrypt_message(self, plaintext: str) -> str | None:
        """
        Encripta un mensaje de texto plano para que sea compatible con Crypto.js.
        El resultado es una cadena en formato Base64.
        """
        if not isinstance(plaintext, str):
            plaintext = str(plaintext)
            
        try:
            plaintext_bytes = plaintext.encode('utf-8')
            salt = get_random_bytes(8)
            key, iv = evp_bytes_to_key(SECRET_KEY, salt, 32, 16) # AES-256
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_plaintext = pad(plaintext_bytes, AES.block_size)
            encrypted_bytes = cipher.encrypt(padded_plaintext)
            
            # Concatena "Salted__", la sal y el texto cifrado, y luego codifica en Base64
            result = b"Salted__" + salt + encrypted_bytes
            return base64.b64encode(result).decode('utf-8')
        except Exception as e:
            print(f"Error al encriptar: {e}")
            return None

    def decrypt_message(self, encrypted_text: str) -> str:
        """
        Desencripta un mensaje encriptado por Crypto.js desde formato Base64.
        """
        if not isinstance(encrypted_text, str):
            return "[Error: el texto a desencriptar no es una cadena]"

        try:
            encrypted_data = base64.b64decode(encrypted_text)
            
            # Extrae la sal (los 8 bytes después de "Salted__")
            if not encrypted_data.startswith(b"Salted__"):
                raise ValueError("Formato de datos encriptados no válido. Falta el prefijo 'Salted__'.")

            salt = encrypted_data[8:16]
            ciphertext = encrypted_data[16:]
            
            key, iv = evp_bytes_to_key(SECRET_KEY, salt, 32, 16) # AES-256
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded_bytes = cipher.decrypt(ciphertext)
            
            # Quita el padding y decodifica a string
            decrypted_bytes = unpad(decrypted_padded_bytes, AES.block_size)
            return decrypted_bytes.decode('utf-8')
        except (ValueError, KeyError) as e:
            # Errores de padding o clave incorrecta
            print(f"Error al desencriptar: {e}")
            return "[Error de desencriptación: clave incorrecta o datos corruptos]"
        except Exception as e:
            print(f"Error inesperado al desencriptar: {e}")
            return "[Error inesperado durante la desencriptación]"
