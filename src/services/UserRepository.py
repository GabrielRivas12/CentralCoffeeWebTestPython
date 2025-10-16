from .repository.IUserRepository import IUserRepository
from ..config.FirebaseConfig import db, excpt

class UserRepositoryImpl(IUserRepository):

    def create_user(self, uid: str, name: str, email: str, location: str, rol: str) -> None:
        try:
            user_ref = db.collection('usuarios').document(uid)
            user_ref.set({
                'uid': uid,
                'nombre': name,
                'correo': email,
                'ubicacion': location,
                'rol': rol
            })
            
        except excpt.FirebaseError as e:
            raise Exception(f"Error creating user in Firestore: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def get_user_by_uid(self, uid: str):
        try:
            user_ref = db.collection('usuarios').document(uid)
            user_doc = user_ref.get()
            if user_doc.exists:
                return user_doc.to_dict()
            else:
                return None
        except excpt.FirebaseError as e:
            raise Exception(f"Error retrieving user from Firestore: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def update_user(self, uid: str, data: dict) -> None:
        try:
            user_ref = db.collection('usuarios').document(uid)
            user_ref.update(data)
        except excpt.FirebaseError as e:
            raise Exception(f"Error updating user in Firestore: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")