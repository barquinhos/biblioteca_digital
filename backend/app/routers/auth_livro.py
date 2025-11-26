from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.livro import LivroCreate, LivroOut, LivroUpdate, QuantidadeExemplaresOut

from backend.app.db_models import Exemplar, Livro
from backend.app.services.livro_service import criar_livro_service, deletar_livro_service, listar_quantidade_exemplares_por_livro

router = APIRouter(prefix="/livros", tags=["livros"])

@router.post("/", response_model=LivroOut, status_code=status.HTTP_201_CREATED)
def criar_livro(payload: LivroCreate, db: Session = Depends(get_db)):
    try:
        return criar_livro_service(db, payload)
    except ValueError as e:
        msg = str(e)
        if msg == "livro nao encontrado":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
        if msg == "Conflito na criação de livro":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Livro já criado.")
        raise e

@router.get("/", response_model=list[LivroOut])
def listar_livros(db: Session = Depends(get_db)):
    try:
        livros = db.query(Livro).all()
        return livros
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar livros: {str(e)}"
        )
    
@router.get("/{livro_id}", response_model=LivroOut)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    return livro

@router.put("/{livro_id}", response_model=LivroOut)
def atualizar_livro(livro_id: int, livro_update: LivroUpdate, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    update_data = livro_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(livro, field, value)
    
    db.commit()
    db.refresh(livro)
    
    return livro

@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    try:
        deletar_livro_service(db, livro_id)
        return None
    except ValueError as e:
        if str(e) == "livro-nao-encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Livro não encontrado"
            )
        raise

@router.get("/{livro_id}/quantidade-exemplares", response_model=QuantidadeExemplaresOut)
def obter_quantidade_exemplares_livro(livro_id: int, db: Session = Depends(get_db)):
    """
    Obtém a quantidade de exemplares de um livro específico
    """
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        if not livro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        
        total = db.query(Exemplar).filter(Exemplar.livro_id == livro_id).count()
        disponiveis = db.query(Exemplar).filter(Exemplar.livro_id == livro_id, Exemplar.status == "disponivel").count()
        emprestados = db.query(Exemplar).filter(Exemplar.livro_id == livro_id, Exemplar.status == "emprestado").count()
        manutencao = db.query(Exemplar).filter(Exemplar.livro_id == livro_id, Exemplar.status == "manutencao").count()
        
        return {
            "livro_id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "total_exemplares": total,
            "disponiveis": disponiveis,
            "emprestados": emprestados,
            "manutencao": manutencao
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter quantidade de exemplares: {str(e)}"
        )