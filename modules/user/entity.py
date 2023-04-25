import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import validates
from core.database import Base
from passlib.hash import pbkdf2_sha256


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    @validates('username')
    def validate_username(self, username):
        if not username:
            raise ValueError('Username cannot be empty')
        if len(username) > 50:
            raise ValueError('Username cannot be longer than 50 characters')
        return username

    @validates('password')
    def validate_password_hash(self, password):
        if not password:
            raise ValueError('Password cannot be empty')
        if len(password) > 100:
            raise ValueError('Password cannot be longer than 100 characters')
        return pbkdf2_sha256.hash(password)

    def verify(self, password) -> bool:
        return pbkdf2_sha256.verify(self.password, password)
