import bcrypt

def generar_password(password_texto):
    # Generar salt y hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_texto.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_password(password_texto, password_hash):
    return bcrypt.checkpw(password_texto.encode('utf-8'), password_hash.encode('utf-8'))

# Generar contraseñas para admin123
password = "admin123"
hash_generado = generar_password(password)

print("=" * 50)
print("GENERADOR DE CONTRASEÑAS")
print("=" * 50)
print(f"Contraseña en texto: {password}")
print(f"Hash generado: {hash_generado}")
print(f"Longitud del hash: {len(hash_generado)}")

# Verificar que funciona
verificacion = verificar_password(password, hash_generado)
print(f"Verificación: {verificacion}")

print("\n📋 Para usar en SQL:")
print(f"INSERT INTO empleado (run, password, nombre, apellido, cargo) VALUES ")
print(f"('12345678-9', '{hash_generado}', 'Admin', 'Sistema', 'gerente');")