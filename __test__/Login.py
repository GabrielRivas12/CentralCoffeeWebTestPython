import unittest
from unittest.mock import MagicMock
import sys
import os

# =========================
# Agregar raíz del proyecto
# =========================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# =========================
# MOCK COMPLETO DE FIREBASE
# =========================
mock_auth_client = MagicMock()
mock_excpt = MagicMock()
mock_firebase_error = type('FirebaseError', (Exception,), {})

# Reemplazar el módulo FirebaseConfig antes de importar AuthRepositoryImpl
sys.modules['src.config.FirebaseConfig'] = MagicMock(authClient=mock_auth_client, excpt=mock_excpt)
sys.modules['src.config.FirebaseConfig'].excpt.FirebaseError = mock_firebase_error

# =========================
# Importar repositorio DESPUÉS de los mocks
# =========================
from src.services.AuthRepositoryImpl import AuthRepositoryImpl

class TestAutenticacionLoginSimulado(unittest.TestCase):

    def setUp(self):
        self.auth_repo = AuthRepositoryImpl()
        mock_auth_client.verify_id_token.reset_mock()
        mock_auth_client.verify_id_token.return_value = None
        mock_auth_client.verify_id_token.side_effect = None

    def test_autenticacion(self):
        token_valido = "token_valido"
        mock_auth_client.verify_id_token.return_value = {
            'uid': 'user123',
            'email': 'usuario@test.com',
            'email_verified': True
        }

        resultado = self.auth_repo.authenticate_user(token_valido)
        mock_auth_client.verify_id_token.assert_called_once_with(token_valido)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['uid'], 'user123')
        self.assertTrue(resultado['email_verified'])
        self.assertEqual(resultado['email'], 'usuario@test.com')

    def test_autenticacion_token_invalido(self):
        token_invalido = "token_invalido"
        mock_auth_client.verify_id_token.side_effect = mock_firebase_error("Token inválido")

        resultado = self.auth_repo.authenticate_user(token_invalido)
        mock_auth_client.verify_id_token.assert_called_once_with(token_invalido)
        self.assertIsNone(resultado)

    def test_autenticacion_email_no_verificado(self):
        token_no_verificado = "token_no_verificado"
        mock_auth_client.verify_id_token.return_value = {
            'uid': 'user456',
            'email': 'noverificado@test.com',
            'email_verified': False
        }

        resultado = self.auth_repo.authenticate_user(token_no_verificado)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['uid'], 'user456')
        self.assertFalse(resultado['email_verified'])

if __name__ == "__main__":
    unittest.main()
