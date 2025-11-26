from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.exemplar import ExemplarCreate, ExemplarOut
from backend.app.services.exemplar_service import criar_exemplar_service, excluir_exemplares_service

router = APIRouter(prefix="/exemplares", tags=["exemplares"])

@router.post("/", response_model=ExemplarOut, status_code=status.HTTP_201_CREATED)
def criar_exemplar(exemplar_data: ExemplarCreate, db: Session = Depends(get_db)):
    try:
        exemplar = criar_exemplar_service(db, exemplar_data)
        return exemplar
    except ValueError as e:
        error_message = str(e)
        if error_message == "livro-nao-encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar exemplar: {str(e)}"
        )
    
@router.delete("/livro/{livro_id}/excluir")
def excluir_exemplares(
    livro_id: int, 
    quantidade: int = Query(..., ge=1, description="Quantidade de exemplares a excluir"),
    db: Session = Depends(get_db)
):
    try:
        resultado = excluir_exemplares_service(db, livro_id, quantidade)
        return resultado
    except ValueError as e:
        error_message = str(e)
        if error_message == "livro-nao-encontrado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Livro não encontrado"
            )
        elif error_message == "quantidade-insuficiente":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não há exemplares disponíveis suficientes para excluir"
            )
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir exemplares: {str(e)}"
        )