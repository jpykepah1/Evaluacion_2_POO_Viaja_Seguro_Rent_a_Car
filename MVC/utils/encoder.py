import bcrypt

class Encoder:
   
    def encode(self, password):
        """Genera hash de contraseña de forma segura"""
        try:
            # Generar salt y hashear la contraseña
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            print(f"❌ Error al encriptar contraseña: {e}")
            return None
   
    def verify(self, password, hashed_password):
        """Verifica si la contraseña coincide con el hash"""
        try:
            if not hashed_password:
                return False
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            print(f"❌ Error al verificar contraseña: {e}")
            return False

    def is_hashed(self, password):
        """Verifica si una cadena ya está hasheada"""
        if not password:
            return False
        return password.startswith('$2b$')