import firebase_admin
from firebase_admin import credentials, firestore, auth, exceptions
from dotenv import get_key

certPath = get_key(".env", "FIREBASE_CERT_PATH")

cred = credentials.Certificate({
                "type": "service_account",
                "project_id": get_key('.env', 'PROJECT_ID'),
                "private_key_id": get_key('.env', 'PRIVATE_KEY_ID'),
                "private_key": get_key('.env', 'PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": get_key('.env', 'CLIENT_EMAIL'),
                "client_id": get_key('.env', 'CLIENT_ID'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            })

default_app = firebase_admin.initialize_app(cred)

db = firestore.client(default_app)

authClient = auth.Client(default_app)

excpt = exceptions
    