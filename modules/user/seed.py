from passlib.handlers.pbkdf2 import pbkdf2_sha256

from core.database import get_db
from modules.user.entity import User


def user_seed():
    session = get_db()
    user = User(username='stone', password=pbkdf2_sha256.hash('P@ssw0rd'))
    session.add(user)
    session.commit()

