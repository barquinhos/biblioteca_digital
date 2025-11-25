from sqlalchemy.orm import Session
from backend.app.db_models import Livro
from backend.app.models.livro import LivroCreate


def criar_livro_service(db: Session, payload: LivroCreate):
    livro_existente = db.query(Livro).filter(
        Livro.titulo.ilike(payload.titulo),
        Livro.autor.ilike(payload.autor)
    ).first()
    
    if livro_existente:
        raise ValueError("Conflito na criação de livro")
    
    novo_livro = Livro(
        titulo=payload.titulo,
        autor=payload.autor,
        ano_publicacao=payload.ano_publicacao,
        editora=payload.editora,
        sinopse=payload.sinopse
    )
    
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    
    return novo_livro

def deletar_livro_service(db: Session, livro_id: int):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    
    if not livro:
        raise ValueError("livro-nao-encontrado")
    
    db.delete(livro)
    db.commit()