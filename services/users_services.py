from models.users_models import User
from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UsersService:
    def get_all_users(self):
        """Obtiene todos los usuarios"""
        return User.query.all()
    
    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID"""
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        """Obtiene un usuario por su nombre de usuario"""
        return User.query.filter_by(username=username).first()
    
    def create_user(self, username, password):
        """Crea un nuevo usuario"""
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def update_user(self, user_id, username=None, password=None):
        """Actualiza un usuario existente"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password)
        
        db.session.commit()
        return user
    
    def delete_user(self, user_id):
        """Elimina un usuario"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    def authenticate_user(self, username, password):
        """Autentica un usuario"""
        user = self.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            return user
        return None
