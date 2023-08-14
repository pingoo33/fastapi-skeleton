import bcrypt
from sqlalchemy import Column, String, Integer

from fastapi_skeleton.common.util.database import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(length=100), unique=True)
    pw = Column(String(length=100))

    @property
    def password(self):
        return self.pw

    @password.setter
    def password(self, password: str):
        self.pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str):
        return bcrypt.checkpw(self.pw.encode('utf-8'), password.encode('utf-8'))

    def sign_up(self, user_id: str, password: str):
        self.user_id = user_id
        self.pw = password
