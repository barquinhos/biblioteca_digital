from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.exemplar import ExemplarCreate, ExemplarOut
from backend.app.services.exemplar_service import criar_exemplar_service

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