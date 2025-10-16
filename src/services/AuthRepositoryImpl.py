from typing import Dict, Optional
from .repository.IAuthRepository import IAuthRepository
from ..config.FirebaseConfig import authClient, excpt


class AuthRepositoryImpl(IAuthRepository):

    def create_user(self, email: str, password: str) -> dict:
        try:
            user = authClient.create_user(
                email=email,
                password=password,
                email_verified=False,
            )

            return{
                'success': True,
                'user': {
                    'uid': user.uid,
                    'email': user.email,
                }
            }
                
        except excpt.FirebaseError as e:
            return {
                'success': False,
                'error': f"error creando el usuario: {str(e)}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"error inesperado: {str(e)}"
            }

    def authenticate_user(self, id_token: str) -> dict:
        try:
            decoded_token = authClient.verify_id_token(id_token)
            
            return decoded_token
        
        except excpt.FirebaseError as e:
            return None

    def get_user(self, uid: str) -> dict:
        try:
            user = authClient.get_user(uid)
            
            return {
                'uid': user.uid,
                'email': user.email,
                'email_verified': user.email_verified,
                'display_name': user.display_name,}
            
        except excpt.FirebaseError as e:
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        try:
            user = authClient.get_user_by_email(email)

            return {
                'uid': user.uid,
                'email': user.email,
                'email_verified': user.email_verified,
                }
            
        except excpt.FirebaseError as e:
            return None

    def delete_user(self, uid: str) -> dict:
        try: 
            authClient.delete_user(uid)
            
            return {'success': True}
        
        except excpt.FirebaseError as e:
            return {
                'success': False,
                'error': f"Error eliminando usuario: {e}"
            }
        
       