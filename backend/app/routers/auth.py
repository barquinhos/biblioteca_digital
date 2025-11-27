from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.db_models import User
from backend.app.models.user import UserCreate, UserOut, UserLogin
from backend.app.utils.security import create_access_token, hash_password, verify_password
from backend.app.services.emprestimo_service import verificar_limite_emprestimos, obter_limite_usuario, obter_emprestimos_ativos_usuario

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

@router.get("/usuarios", response_model=list[UserOut]) 
def listar_todos_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = db.query(User).all()
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar usuários: {str(e)}"
        )
    
@router.get("/usuarios/pesquisar/{tipo}", response_model=list[UserOut])
def pesquisar_usuarios_por_tipo(tipo: str, db: Session = Depends(get_db)):
    try:
        usuarios = db.query(User).filter(User.tipo.ilike(f"%{tipo}%")).all()
        
        if not usuarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum usuário do tipo '{tipo}' encontrado"
            )
            
        return usuarios
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao pesquisar usuários: {str(e)}"
        )
    
@router.delete("/usuarios/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(user_id: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(User).filter(User.id == user_id).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        db.delete(usuario)
        db.commit()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )
    
@router.get("/usuarios/{user_id}/status-emprestimos")
def status_emprestimos_usuario(user_id: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(User).filter(User.id == user_id).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        limite = obter_limite_usuario(usuario.tipo)
        emprestimos_ativos = obter_emprestimos_ativos_usuario(db, user_id)
        disponivel_para_emprestimo = verificar_limite_emprestimos(db, user_id)
        
        return {
            "usuario_id": user_id,
            "nome": usuario.nome,
            "tipo": usuario.tipo,
            "limite_emprestimos": "Ilimitado" if limite == -1 else limite,
            "emprestimos_ativos": emprestimos_ativos,
            "disponivel_para_emprestimo": disponivel_para_emprestimo,
            "mensagem": f"Usuário pode emprestar {'mais livros' if disponivel_para_emprestimo else '0 livros (limite atingido)'}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar status: {str(e)}"
        )