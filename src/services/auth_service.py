from repositories.user import UserRepository
from passlib.hash import bcrypt

class AuthService:
    def __init__(self) :
        self.repo = UserRepository()

    def register_user(self, first_name: str, last_name: str, email: str, password: str, role: str = "user") :
        if self.repo.get_user_by_email(email):
            raise ValueError("Пользователь с таким email уже существует")

        hashed_password = bcrypt.hash(password)

        self.repo.add_user(first_name, last_name, email, hashed_password, role)
        print(f"Пользователь {email} успешно зарегистрирован")

    def authenticate_user(self, email: str, password: str) :
        user = self.repo.get_user_by_email(email)
        if user and bcrypt.verify(password, user[4]):
            return user
        return None
    
    def get_user_info(self, user_id): 
        return self.repo.get_user_info(user_id)
