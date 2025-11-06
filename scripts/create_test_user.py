#!/usr/bin/env python
"""Script útil para crear un usuario de prueba en la base de datos.
Uso:
  python scripts/create_test_user.py --username admin --password secret
"""
import argparse
from werkzeug.security import generate_password_hash
from config.database import get_db_session
from repositories.users_repository import get_by_username, create_user


def main():
    parser = argparse.ArgumentParser(description='Crear usuario de prueba')
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    args = parser.parse_args()

    session = get_db_session()
    try:
        existing = get_by_username(session, args.username)
        if existing:
            print(f"El usuario '{args.username}' ya existe (id={existing.id}).")
            return
        pwd_hash = generate_password_hash(args.password)
        user = create_user(session, args.username, pwd_hash)
        print(f"Usuario creado: {user.username} (id={user.id})")
    except Exception as e:
        print('Error al crear usuario:', e)
    finally:
        session.close()


if __name__ == '__main__':
    main()
