import secrets
import string

def generar_token(longitud=32):
    """
    Genera un token aleatorio seguro
    
    Args:
        longitud (int): Longitud deseada del token (por defecto 32 caracteres)
    
    Returns:
        str: Token generado
    """
    # Definir los caracteres permitidos
    caracteres = string.ascii_letters + string.digits + '-_'
    
    # Generar el token usando secrets para mayor seguridad
    token = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    
    return token

if __name__ == '__main__':
    # Ejemplo de uso
    token = generar_token()
    print(f"Token generado: {token}")
