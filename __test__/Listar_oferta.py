import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# ============================
# Agregar solo la raíz del proyecto
# ============================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ============================
# Bloquear Firebase y Supabase completamente
# ============================
sys.modules['src.config.FirebaseConfig'] = MagicMock()
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()
sys.modules['firebase_admin.firestore'] = MagicMock()
sys.modules['src.config.SupabaseConfig'] = MagicMock()
sys.modules['supabase'] = MagicMock()
sys.modules['supabase._sync.client'] = MagicMock()


class TestOfertasController(unittest.TestCase):

    def setUp(self):
        """Configurar mocks independientes antes de cada test"""
        # Mock de OffersRepositoryImpl
        self.mock_offers_repo = MagicMock()
        self.mock_offers_repo.obtener_todos.return_value = [
            {'titulo': 'Café Test', 'id': '1', 'estado': 'Activo'}
        ]
        self.mock_offers_repo.obtener_lugares.return_value = [{'nombre': 'Finca Test'}]

        # Mock de UserRepository
        self.mock_user_repo = MagicMock()
        self.mock_user_repo.get_user_by_uid.return_value = {'nombre': 'Test User'}

        # Importar y configurar el controlador con nuestros mocks
        from src.controllers.OffersController import configure_repositories
        configure_repositories(
            offers_repo=self.mock_offers_repo,
            user_repo=self.mock_user_repo
        )
        
        # Ahora importar las referencias a los repositorios
        from src.controllers.OffersController import repository, usrRepository
        self.repository = repository
        self.usrRepository = usrRepository

    def test_obtener_todos_mock_directo(self):
        """Prueba directa usando solo mocks"""
        resultado = self.repository.obtener_todos()
        self.mock_offers_repo.obtener_todos.assert_called_once()
        self.assertEqual(resultado[0]['titulo'], 'Café Test')

    def test_integracion_completa_simple(self):
        """Prueba de integración usando solo mocks"""
        ofertas = self.repository.obtener_todos()
        user = self.usrRepository.get_user_by_uid("test123")

        self.mock_offers_repo.obtener_todos.assert_called_once()
        self.mock_user_repo.get_user_by_uid.assert_called_once_with("test123")

        self.assertEqual(ofertas[0]['titulo'], 'Café Test')
        self.assertEqual(user['nombre'], 'Test User')

    def test_flujo_completo_listar_ofertas(self):
        """Prueba flujo completo con múltiples datos"""
        # Reconfigurar datos simulados para este test
        test_user = {'uid': 'user123', 'nombre': 'Gabriel'}
        test_ofertas = [
            {'id': '1', 'titulo': 'Café Supremo', 'estado': 'Activo'},
            {'id': '2', 'titulo': 'Café Gourmet', 'estado': 'Inactivo'}
        ]
        test_lugares = [
            {'id': 'l1', 'nombre': 'Finca Central'},
            {'id': 'l2', 'nombre': 'Finca Norte'}
        ]

        self.mock_user_repo.get_user_by_uid.return_value = test_user
        self.mock_offers_repo.obtener_todos.return_value = test_ofertas
        self.mock_offers_repo.obtener_lugares.return_value = test_lugares

        user = self.usrRepository.get_user_by_uid("user123")
        ofertas = self.repository.obtener_todos()
        lugares = self.repository.obtener_lugares()

        self.assertEqual(user, test_user)
        self.assertEqual(ofertas, test_ofertas)
        self.assertEqual(lugares, test_lugares)
        
        # Verificar que se llamaron los métodos
        self.mock_user_repo.get_user_by_uid.assert_called_once_with("user123")
        self.mock_offers_repo.obtener_todos.assert_called_once()
        self.mock_offers_repo.obtener_lugares.assert_called_once()


if __name__ == "__main__":
    unittest.main()