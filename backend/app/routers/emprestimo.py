from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.database import get_db
from backend.app.models.emprestimo import EmprestimoCreate, EmprestimoOut
from backend.app.services.emprestimo_service import (
    criar_emprestimo_service,
    obter_emprestimos_ativos_usuario,
    obter_limite_usuario
)
from backend.app.db_models import Emprestimo, User

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

@router.post("/", response_model=EmprestimoOut, status_code=status.HTTP_201_CREATED)
def criar_emprestimo(emprestimo_data: EmprestimoCreate, db: Session = Depends(get_db)):
    try:
        emprestimo = criar_emprestimo_service(db, emprestimo_data)
        return emprestimo
    except ValueError as e:
        error_message = str(e)
        if error_message == "usuário-nao-encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        elif error_message == "exemplar-nao-encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exemplar não encontrado"
            )
        elif error_message == "exemplar-indisponivel":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exemplar não está disponível para empréstimo"
            )
        elif error_message == "limite-emprestimos-atingido":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário atingiu o limite de empréstimos"
            )
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar empréstimo: {str(e)}"
        )

@router.get("/", response_model=List[EmprestimoOut])
def listar_emprestimos(
    usuario_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Emprestimo)
        
        if usuario_id:
            query = query.filter(Emprestimo.usuario_id == usuario_id)
        
        if status:
            query = query.filter(Emprestimo.status == status)
        
        emprestimos = query.all()
        return emprestimos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar empréstimos: {str(e)}"
        )

@router.get("/{emprestimo_id}", response_model=EmprestimoOut)
def obter_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado"
        )
    return emprestimo

@router.get("/usuarios/{usuario_id}/limites")
def obter_limites_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(User).filter(User.id == usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        emprestimos_ativos = obter_emprestimos_ativos_usuario(db, usuario_id)
        limite = obter_limite_usuario(usuario.tipo)
        
        return {
            "usuario_id": usuario_id,
            "tipo_usuario": usuario.tipo,
            "emprestimos_ativos": emprestimos_ativos,
            "limite": limite,
            "pode_emprestar": limite == -1 or emprestimos_ativos < limite
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter limites do usuário: {str(e)}"
        )