import unittest
from Metodos.Usuarios import Usuarios

class UsuariosUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.usuarios_service = Usuarios()

    def test_validate_email_valid(self):
        """Unit Test: email validation passes for correct email"""
        # Debe pasar sin lanzar excepcion
        self.usuarios_service._validate_email("test@gmail.com")

    def test_validate_email_invalid_format(self):
        """Unit Test: email validation fails for bad format"""
        with self.assertRaises(ValueError) as context:
            self.usuarios_service._validate_email("invalid-email")
        self.assertTrue("Invalid email format" in str(context.exception))

    def test_validate_email_invalid_provider(self):
        """Unit Test: email validation fails for unauthorized provider"""
        with self.assertRaises(ValueError) as context:
            self.usuarios_service._validate_email("test@unauthorized.com")
        self.assertTrue("Email provider not allowed" in str(context.exception))

    def test_validate_password_valid(self):
        """Unit Test: password validation passes for valid length"""
        self.usuarios_service._validate_password("SecurePass123!")

    def test_validate_password_invalid(self):
        """Unit Test: password validation fails for short length"""
        with self.assertRaises(ValueError) as context:
            self.usuarios_service._validate_password("short")
        self.assertTrue("Password must be at least 8 characters" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
