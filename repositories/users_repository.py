from models.users_models import User


def get_by_username(session, username: str):
    """Retorna la instancia User cuyo username coincide, o None si no existe."""
    return session.query(User).filter(User.username == username).first()


def create_user(session, username: str, password: str):
    """Helper para crear un usuario (usa si es necesario en el futuro)."""
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
