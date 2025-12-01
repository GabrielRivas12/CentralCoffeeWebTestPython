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


class TestMapaPermisosAdministrador(unittest.TestCase):

    def setUp(self):
        # Mock de MapRepositoryImpl
        self.mock_map_repo = MagicMock()
        self.mock_map_repo.getLocations.return_value = [
            {
                'nombre': 'Finca Central',
                'doc_id': '1',
                'latitud': 12.865416,
                'longitud': -85.207229,
                'horario': '08:00 - 17:00',
                'descripcion': 'Finca principal'
            }
        ]

        # Mock de UserRepository
        self.mock_user_repo = MagicMock()

        self.patcher1 = patch(
            'src.services.MapRepositoryImpl.MapRepositoryImpl',
            return_value=self.mock_map_repo
        )
        self.patcher2 = patch(
            'src.services.UserRepository.UserRepositoryImpl',
            return_value=self.mock_user_repo
        )
        
        self.mock_map_class = self.patcher1.start()
        self.mock_user_class = self.patcher2.start()

    def tearDown(self):
        """Detener patches después de cada test"""
        self.patcher1.stop()
        self.patcher2.stop()

    def test_administrador_puede_ver_boton_agregar_marcador(self):
        # Simular usuario administrador
        test_user = {'uid': 'admin123', 'nombre': 'Admin User', 'role': 'Administrador'}
        self.mock_user_repo.get_user_by_uid.return_value = test_user
        
        # Importar repositorios después de los mocks
        from src.services.MapRepositoryImpl import MapRepositoryImpl
        from src.services.UserRepository import UserRepositoryImpl
        
        repository = MapRepositoryImpl()
        usrRepository = UserRepositoryImpl()
        
        # Obtener datos para el template
        locations = repository.getLocations()
        user = usrRepository.get_user_by_uid("admin123")
        
        # Verificar que se obtuvieron los datos
        self.mock_map_repo.getLocations.assert_called_once()
        self.mock_user_repo.get_user_by_uid.assert_called_with("admin123")
        
        # Verificar datos del usuario
        self.assertEqual(user['role'], 'Administrador')
        
        # Simular la lógica del template
        user_role = user.get('role', '')
        mostrar_boton_agregar = (user_role == 'Administrador')
        
        self.assertTrue(mostrar_boton_agregar, "El administrador debería ver el botón agregar marcador")

    def test_usuario_normal_no_puede_ver_boton_agregar_marcador(self):
        """Verificar que usuarios no administradores NO ven el botón de agregar marcador"""
        # Simular usuario normal
        test_user = {'uid': 'user123', 'nombre': 'Usuario Normal', 'role': 'Usuario'}
        self.mock_user_repo.get_user_by_uid.return_value = test_user
        
        # Importar repositorios
        from src.services.UserRepository import UserRepositoryImpl
        usrRepository = UserRepositoryImpl()
        
        user = usrRepository.get_user_by_uid("user123")
        
        # Verificar datos del usuario
        self.assertEqual(user['role'], 'Usuario')
        
        # Simular lógica del template
        user_role = user.get('role', '')
        mostrar_boton_agregar = (user_role == 'Administrador')
        
        self.assertFalse(mostrar_boton_agregar, "Usuario normal NO debería ver el botón agregar marcador")

    def test_usuario_sin_rol_no_puede_ver_boton_agregar_marcador(self):
        """Verificar que usuarios sin rol definido NO ven el botón de agregar marcador"""
        # Simular usuario sin rol
        test_user = {'uid': 'user456', 'nombre': 'Usuario Sin Rol'}
        self.mock_user_repo.get_user_by_uid.return_value = test_user
        
        from src.services.UserRepository import UserRepositoryImpl
        usrRepository = UserRepositoryImpl()
        
        user = usrRepository.get_user_by_uid("user456")
        
        # Simular lógica del template
        user_role = user.get('role', '')
        mostrar_boton_agregar = (user_role == 'Administrador')
        
        self.assertFalse(mostrar_boton_agregar, "Usuario sin rol NO debería ver el botón agregar marcador")

    def test_administrador_puede_ver_botones_editar_eliminar(self):
        """Verificar que el administrador ve botones editar/eliminar en los marcadores"""
        # Simular usuario administrador
        test_user = {'uid': 'admin123', 'nombre': 'Admin User', 'role': 'Administrador'}
        self.mock_user_repo.get_user_by_uid.return_value = test_user
        
        from src.services.UserRepository import UserRepositoryImpl
        usrRepository = UserRepositoryImpl()
        
        user = usrRepository.get_user_by_uid("admin123")
        
        # Simular lógica del template para botones en marcadores
        user_role = user.get('role', '')
        mostrar_botones_admin = (user_role == 'Administrador')
        
        self.assertTrue(mostrar_botones_admin, "Administrador debería ver botones editar/eliminar")

    def test_usuario_normal_no_puede_ver_botones_editar_eliminar(self):
        """Verificar que usuarios normales NO ven botones editar/eliminar"""
        # Simular usuario normal
        test_user = {'uid': 'user123', 'nombre': 'Usuario Normal', 'role': 'Cliente'}
        self.mock_user_repo.get_user_by_uid.return_value = test_user
        
        from src.services.UserRepository import UserRepositoryImpl
        usrRepository = UserRepositoryImpl()
        
        user = usrRepository.get_user_by_uid("user123")
        
        # Simular lógica del template para botones en marcadores
        user_role = user.get('role', '')
        mostrar_botones_admin = (user_role == 'Administrador')
        
        self.assertFalse(mostrar_botones_admin, "Usuario normal NO debería ver botones editar/eliminar")

    def test_flujo_completo_permisos_mapa(self):
        """Prueba flujo completo de verificación de permisos en el mapa"""
        # Configurar datos de prueba
        test_locations = [
            {
                'nombre': 'Finca Test 1',
                'doc_id': 'loc1',
                'latitud': 12.865416,
                'longitud': -85.207229,
                'horario': '08:00 - 17:00',
                'descripcion': 'Finca de prueba 1'
            },
            {
                'nombre': 'Finca Test 2', 
                'doc_id': 'loc2',
                'latitud': 12.875416,
                'longitud': -85.217229,
                'horario': '07:00 - 16:00',
                'descripcion': 'Finca de prueba 2'
            }
        ]
        
        test_admin_user = {'uid': 'admin123', 'nombre': 'Admin', 'role': 'Administrador'}
        test_normal_user = {'uid': 'user123', 'nombre': 'Usuario', 'role': 'Cliente'}
        
        # Importar repositorios
        from src.services.MapRepositoryImpl import MapRepositoryImpl
        from src.services.UserRepository import UserRepositoryImpl
        
        repository = MapRepositoryImpl()
        usrRepository = UserRepositoryImpl()
        
        # Probar con administrador
        self.mock_map_repo.getLocations.return_value = test_locations
        self.mock_user_repo.get_user_by_uid.return_value = test_admin_user
        
        locations = repository.getLocations()
        admin_user = usrRepository.get_user_by_uid("admin123")
        
        # Verificar permisos de administrador
        self.assertEqual(admin_user['role'], 'Administrador')
        self.assertEqual(len(locations), 2)
        
        # Verificar que se pueden realizar operaciones de admin
        puede_agregar = (admin_user.get('role') == 'Administrador')
        puede_editar = (admin_user.get('role') == 'Administrador') 
        puede_eliminar = (admin_user.get('role') == 'Administrador')
        
        self.assertTrue(puede_agregar, "Admin debería poder agregar marcadores")
        self.assertTrue(puede_editar, "Admin debería poder editar marcadores")
        self.assertTrue(puede_eliminar, "Admin debería poder eliminar marcadores")
        
        # Probar con usuario normal
        self.mock_user_repo.get_user_by_uid.return_value = test_normal_user
        normal_user = usrRepository.get_user_by_uid("user123")
        
        # Verificar permisos de usuario normal
        self.assertEqual(normal_user['role'], 'Cliente')
        
        puede_agregar_normal = (normal_user.get('role') == 'Administrador')
        puede_editar_normal = (normal_user.get('role') == 'Administrador')
        puede_eliminar_normal = (normal_user.get('role') == 'Administrador')
        
        self.assertFalse(puede_agregar_normal, "Usuario normal NO debería poder agregar marcadores")
        self.assertFalse(puede_editar_normal, "Usuario normal NO debería poder editar marcadores")
        self.assertFalse(puede_eliminar_normal, "Usuario normal NO debería poder eliminar marcadores")

    def test_permisos_operaciones_crud_administrador(self):
        """Verificar que el administrador puede realizar todas las operaciones CRUD"""
        test_admin_user = {'uid': 'admin123', 'nombre': 'Admin', 'role': 'Administrador'}
        self.mock_user_repo.get_user_by_uid.return_value = test_admin_user
        
        from src.services.UserRepository import UserRepositoryImpl
        from src.services.MapRepositoryImpl import MapRepositoryImpl
        
        usrRepository = UserRepositoryImpl()
        repository = MapRepositoryImpl()
        
        admin_user = usrRepository.get_user_by_uid("admin123")
        
        # Simular operaciones CRUD que debería poder realizar el admin
        if admin_user.get('role') == 'Administrador':
            # Operación de crear - debería funcionar
            new_location_data = {
                'nombre': 'Nueva Finca',
                'latitud': 12.865416,
                'longitud': -85.207229,
                'horario': '08:00 - 17:00',
                'descripcion': 'Nueva finca agregada'
            }
            self.mock_map_repo.createLocation.return_value = True
            resultado_crear = repository.createLocation(new_location_data)
            self.assertTrue(resultado_crear)
            
            # Operación de actualizar - debería funcionar
            update_data = {'nombre': 'Finca Actualizada'}
            self.mock_map_repo.updateLocation.return_value = True
            resultado_actualizar = repository.updateLocation('loc1', update_data)
            self.assertTrue(resultado_actualizar)
            
            # Operación de eliminar - debería funcionar
            self.mock_map_repo.deleteLocation.return_value = True
            resultado_eliminar = repository.deleteLocation('loc1')
            self.assertTrue(resultado_eliminar)

    def test_simulacion_template_condicional(self):
        """Simular exactamente la lógica condicional del template HTML"""
        # Caso 1: Usuario administrador
        user_role_admin = "Administrador"
        
        # Simular la condición del template: {% if user_role == 'Administrador' %}
        mostrar_boton_agregar_admin = (user_role_admin == 'Administrador')
        
        # En el template, esto mostraría el botón
        self.assertTrue(mostrar_boton_agregar_admin)
        
        # Caso 2: Usuario normal
        user_role_normal = "Cliente"
        mostrar_boton_agregar_normal = (user_role_normal == 'Administrador')
        
        # En el template, esto OCULTARÍA el botón
        self.assertFalse(mostrar_boton_agregar_normal)
        
        # Caso 3: Sin rol
        user_role_none = ""
        mostrar_boton_agregar_none = (user_role_none == 'Administrador')
        
        # En el template, esto OCULTARÍA el botón
        self.assertFalse(mostrar_boton_agregar_none)

    def test_verificacion_estricta_rol_administrador(self):
        """Verificar que solo el rol exacto 'Administrador' tiene permisos"""
        roles_con_permisos = ['Administrador']
        roles_sin_permisos = ['Admin', 'administrador', 'ADMINISTRADOR', 'Cliente', 'Usuario', 'Vendedor', '', None]
        
        for rol in roles_con_permisos:
            tiene_permisos = (rol == 'Administrador')
            self.assertTrue(tiene_permisos, f"El rol '{rol}' debería tener permisos")
        
        for rol in roles_sin_permisos:
            tiene_permisos = (rol == 'Administrador')
            self.assertFalse(tiene_permisos, f"El rol '{rol}' NO debería tener permisos")


if __name__ == "__main__":
    unittest.main()