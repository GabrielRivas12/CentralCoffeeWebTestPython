import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import get_key

certPath = get_key(".env", "FIREBASE_CERT_PATH")

cred = credentials.Certificate(certPath)
default_app = firebase_admin.initialize_app(cred)

db = firestore.client(default_app)


