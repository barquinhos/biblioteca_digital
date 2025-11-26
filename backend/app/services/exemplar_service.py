from sqlalchemy.orm import Session
from backend.app.db_models import Exemplar, Livro
from backend.app.models.exemplar import ExemplarCreate
from .livro_service import gerar_codigo_exemplar, obter_proximo_numero_sequencial

def criar_exemplar_service(db: Session, exemplar_data: ExemplarCreate):
    livro = db.query(Livro).filter(Livro.id == exemplar_data.livro_id).first()
    if not livro:
        raise ValueError("livro-nao-encontrado")
    
    numero_sequencial = obter_proximo_numero_sequencial(db, exemplar_data.livro_id)
    codigo_gerado = gerar_codigo_exemplar(livro.titulo, numero_sequencial)
    
    novo_exemplar = Exemplar(
        codigo=codigo_gerado,
        livro_id=exemplar_data.livro_id,
        status="disponivel"
    )
    
    db.add(novo_exemplar)
    db.commit()
    db.refresh(novo_exemplar)
    
    return novo_exemplar

def excluir_exemplares_service(db: Session, livro_id: int, quantidade: int):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise ValueError("livro-nao-encontrado")
    
    exemplares_para_excluir = db.query(Exemplar).filter(
        Exemplar.livro_id == livro_id,
        Exemplar.status == "disponivel"
    ).limit(quantidade).all()
    
    if len(exemplares_para_excluir) < quantidade:
        raise ValueError("quantidade-insuficiente")
    
    for exemplar in exemplares_para_excluir:
        db.delete(exemplar)
    
    db.commit()
    
    return {
        "livro_id": livro_id,
        "exemplares_excluidos": quantidade,
        "titulo_livro": livro.titulo
    }