from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.db_models import User
from backend.app.models.user import UserCreate, UserOut, UserLogin
from backend.app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
   nome_norm = payload.nome.strip()
   email_norm = payload.email

   exists = (
      db.query(User)
      .filter(or_(
         func.lower(User.nome) == func.lower(nome_norm),    
         func.lower(User.email) == func.lower(email_norm)
         )
      ).first()
   )

   if exists:
      raise HTTPException(
         status_code=409,
         detail="nome/email já cadastrado"
      )
   
   user = User(
      nome=payload.nome,
      matricula=payload.matricula,
      email=email_norm,
      tipo=payload.tipo,
      # status="ativo",
      password_hash=hash_password(payload.senha)
   )

   db.add(user)
   db.commit()
   db.refresh(user)

   return user

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
   user = db.query(User).filter(User.email == payload.email).first()
    
   if not user or not verify_password(payload.senha, user.password_hash):  # ⬅️ CORRIGIDO: payload.senha
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )
    
   access_token = create_access_token(
       subject={"sub": user.email, "user_id": user.id}
   )

   return {
       "access_token": access_token,
       "token_type": "bearer",
       "user": {
           "id": user.id,
           "nome": user.nome,
           "email": user.email,
           "tipo": user.tipo
       }
   }