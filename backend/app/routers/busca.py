from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.livro_service import buscar_livros_service

router = APIRouter(prefix="/busca", tags=["busca"])

@router.get("/livros")
def buscar_livros(q: str = Query(..., description="Termo para buscar"), db: Session = Depends(get_db)):
    livros = buscar_livros_service(db, q)
    return livros