import firebase_admin
from firebase_admin import credentials, firestore

# Ruta al archivo JSON de la cuenta de servicio
cred = credentials.Certificate("config/centralcoffee-2910d-firebase-adminsdk-fbsvc-dba8525d73.json")

# Inicializa la app de Firebase Admin
firebase_admin.initialize_app(cred)

# Conexión a Firestore
db = firestore.client()
