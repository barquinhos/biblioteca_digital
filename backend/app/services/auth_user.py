from backend.app.models.user import UserLogin
from backend.app.db_models import User
from backend.app.utils.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from sqlalchemy import func


def authenticate_user(db: Session, payload: UserLogin) -> tuple[User, str]:
    ident = payload.email.strip()
    query = db.query(User)
    user = query.filter(func.lower(User.email) == ident.lower()).first()
    # print(user.email)

    if not user:
        raise ValueError("invalid-credentials")

    if not verify_password(payload.password, user.password_hash):
        raise ValueError("invalid-credentials")
    
    token = create_access_token({"sub": str(user.id), "name": user.name, "email": user.email})

    return user