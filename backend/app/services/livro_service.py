from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict

from backend.app.db_models import Exemplar, Livro
from backend.app.models.livro import LivroCreate

from unidecode import unidecode
import re


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

def gerar_codigo_exemplar(titulo_livro: str, numero_sequencial: int) -> str:
    titulo_limpo = unidecode(titulo_livro)
    
    palavras_ignorar = {'de', 'da', 'do', 'das', 'dos', 'e', 'em', 'no', 'na', 'nos', 'nas', 'um', 'uma', 'o', 'a'}
    
    iniciais = []
    for palavra in titulo_limpo.upper().split():
        palavra_limpa = re.sub(r'[^A-Z]', '', palavra)
        if palavra_limpa and palavra_limpa not in palavras_ignorar:
            iniciais.append(palavra_limpa[0])
    
    if not iniciais:
        iniciais = list(titulo_limpo.upper().replace(' ', '')[:3])
    
    sigla = ''.join(iniciais[:3])
    
    numero_formatado = f"{numero_sequencial:03d}"
    
    return f"{sigla}-{numero_formatado}"

def obter_proximo_numero_sequencial(db: Session, livro_id: int) -> int:
    ultimo_exemplar = db.query(Exemplar).filter(
        Exemplar.livro_id == livro_id
    ).order_by(Exemplar.id.desc()).first()
    
    if ultimo_exemplar:
        codigo_atual = ultimo_exemplar.codigo
        partes = codigo_atual.split('-')
        if len(partes) == 2 and partes[1].isdigit():
            return int(partes[1]) + 1
    
    return 1 

def listar_quantidade_exemplares_por_livro(db: Session) -> List[Dict]:
    resultado = db.query(
        Livro.id,
        Livro.titulo,
        Livro.autor,
        func.count(Exemplar.id).label('total_exemplares'),
        func.sum(func.case((Exemplar.status == 'disponivel', 1), else_=0)).label('disponiveis'),
        func.sum(func.case((Exemplar.status == 'emprestado', 1), else_=0)).label('emprestados'),
        func.sum(func.case((Exemplar.status == 'manutencao', 1), else_=0)).label('manutencao')
    ).join(
        Exemplar, Livro.id == Exemplar.livro_id
    ).group_by(
        Livro.id, Livro.titulo, Livro.autor
    ).all()
    
    return [
        {
            "livro_id": livro_id,
            "titulo": titulo,
            "autor": autor,
            "total_exemplares": total_exemplares,
            "disponiveis": disponiveis or 0,
            "emprestados": emprestados or 0,
            "manutencao": manutencao or 0
        }
        for livro_id, titulo, autor, total_exemplares, disponiveis, emprestados, manutencao in resultado
    ]