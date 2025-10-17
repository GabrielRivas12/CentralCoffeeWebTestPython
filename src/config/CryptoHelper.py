import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

class CryptoJSCompatible:
    """
    Clase para encriptar y desencriptar mensajes compatibles con CryptoJS
    """
    
    def __init__(self, key: str):
        """
        Inicializa con una clave secreta
        
        Args:
            key (str): Clave secreta para encriptación
        """
        self.key = key.encode('utf-8')
        # CryptoJS usa SHA256 para derivar la clave
        self.derived_key = hashlib.sha256(self.key).digest()
    
    def encrypt(self, message: str) -> str:
        """
        Encripta un mensaje de forma compatible con CryptoJS
        
        Args:
            message (str): Mensaje a encriptar
            
        Returns:
            str: Mensaje encriptado en formato Base64
        """
        try:
            # Convertir mensaje a bytes
            message_bytes = message.encode('utf-8')
            
            # Generar IV aleatorio (16 bytes para AES)
            iv = get_random_bytes(16)
            
            # Crear cipher AES en modo CBC
            cipher = AES.new(self.derived_key, AES.MODE_CBC, iv)
            
            # Aplicar padding PKCS7 y encriptar
            encrypted = cipher.encrypt(pad(message_bytes, AES.block_size))
            
            # Combinar IV + datos encriptados
            combined = iv + encrypted
            
            # Codificar en Base64
            encrypted_base64 = base64.b64encode(combined).decode('utf-8')
            
            return encrypted_base64
            
        except Exception as e:
            raise Exception(f"Error en encriptación: {e}")
    
    def decrypt(self, encrypted_message: str) -> str:
        """
        Desencripta un mensaje encriptado con CryptoJS
        
        Args:
            encrypted_message (str): Mensaje encriptado en Base64
            
        Returns:
            str: Mensaje desencriptado
        """
        try:
            # Decodificar Base64
            encrypted_bytes = base64.b64decode(encrypted_message)
            
            # Extraer IV (primeros 16 bytes)
            iv = encrypted_bytes[:16]
            
            # Extraer datos encriptados (resto)
            encrypted_data = encrypted_bytes[16:]
            
            # Crear cipher AES en modo CBC
            cipher = AES.new(self.derived_key, AES.MODE_CBC, iv)
            
            # Desencriptar y remover padding
            decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
            
            # Convertir a string
            return decrypted.decode('utf-8')
            
        except Exception as e:
            raise Exception(f"Error en desencriptación: {e}")
    
    def encrypt_to_json(self, message: str) -> str:
        """
        Encripta y devuelve en formato JSON compatible con CryptoJS
        
        Returns:
            str: JSON con datos encriptados
        """
        encrypted = self.encrypt(message)
        
        # Formato similar al que usa CryptoJS
        result = {
            'ct': encrypted,  # cipher text
            'iv': base64.b64encode(get_random_bytes(16)).decode('utf-8'),  # dummy, ya incluido en ct
            's': ''  # salt (vacío para compatibilidad)
        }
        
        return json.dumps(result)
    
    def decrypt_from_json(self, json_data: str) -> str:
        """
        Desencripta desde formato JSON de CryptoJS
        
        Args:
            json_data (str): JSON con datos encriptados
            
        Returns:
            str: Mensaje desencriptado
        """
        try:
            data = json.loads(json_data)
            
            if 'ct' in data:
                return self.decrypt(data['ct'])
            else:
                raise ValueError("Formato JSON inválido: falta campo 'ct'")
                
        except json.JSONDecodeError:
            # Si no es JSON, intentar desencriptar directamente
            return self.decrypt(json_data)

# Versión con gestión de instancias
class EncryptionManager:
    """
    Gestor de encriptación para toda la aplicación
    """
    
    _instance = None
    
    def __init__(self, secret_key: str = None):
        if secret_key is None:
            # Clave por defecto (deberías usar una variable de entorno)
            secret_key = 'tu_clave_secreta_32_caracteres!!!'
        
        self.crypto = CryptoJSCompatible(secret_key)
    
    @classmethod
    def get_instance(cls, secret_key: str = None):
        """Patrón Singleton para obtener instancia única"""
        if cls._instance is None:
            cls._instance = cls(secret_key)
        return cls._instance
    
    def encrypt_message(self, message: str, format: str = "base64") -> str:
        """
        Encripta un mensaje
        
        Args:
            message (str): Mensaje a encriptar
            format (str): Formato de salida: "base64" o "json"
            
        Returns:
            str: Mensaje encriptado
        """
        if format == "json":
            return self.crypto.encrypt_to_json(message)
        else:
            return self.crypto.encrypt(message)
    
    def decrypt_message(self, encrypted_message: str) -> str:
        """
        Desencripta un mensaje (detecta automáticamente el formato)
        
        Args:
            encrypted_message (str): Mensaje encriptado
            
        Returns:
            str: Mensaje desencriptado
        """
        return self.crypto.decrypt_from_json(encrypted_message)
    
    def is_encrypted(self, text: str) -> bool:
        """
        Verifica si un texto parece estar encriptado
        """
        try:
            # Intentar decodificar Base64
            base64.b64decode(text)
            return True
        except:
            try:
                # Verificar si es JSON de CryptoJS
                data = json.loads(text)
                return 'ct' in data
            except:
                return False