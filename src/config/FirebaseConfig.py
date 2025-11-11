import os
import firebase_admin
from firebase_admin import credentials, firestore, auth, exceptions
from google.cloud.firestore_v1 import base_query


cred = credentials.Certificate({
                "type": "service_account",
                "project_id": os.environ.get('PROJECT_ID'),
                "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
                "private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": os.environ.get('CLIENT_EMAIL'),
                "client_id": os.environ.get('CLIENT_ID'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            })

default_app = firebase_admin.initialize_app(cred)

db = firestore.client(default_app)

authClient = auth.Client(default_app)

excpt = exceptions

query = base_query


    