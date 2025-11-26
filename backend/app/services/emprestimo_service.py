from sqlalchemy.orm import Session

from backend.app.db_models import User, Emprestimo, Exemplar
from backend.app.models.emprestimo import EmprestimoCreate

from typing import Dict

LIMITES_EMPRESTIMOS: Dict[str, int] = {
    "aluno": 5,           
    "professor": 10,     
    "bibliotecario": -1,        
}

def criar_emprestimo_service(db: Session, emprestimo_data: EmprestimoCreate):
    usuario = db.query(User).filter(User.id == emprestimo_data.usuario_id).first()
    if not usuario:
        raise ValueError("usuário-nao-encontrado")
    
    exemplar = db.query(Exemplar).filter(Exemplar.id == emprestimo_data.exemplar_id).first()
    if not exemplar:
        raise ValueError("exemplar-nao-encontrado")
    
    if exemplar.status != "disponivel":
        raise ValueError("exemplar-indisponivel")
    
    if not verificar_limite_emprestimos(db, emprestimo_data.usuario_id):
        raise ValueError("limite-emprestimos-atingido")
    
    novo_emprestimo = Emprestimo(
        usuario_id=emprestimo_data.usuario_id,
        exemplar_id=emprestimo_data.exemplar_id,
        data_devolucao_prevista=emprestimo_data.data_devolucao_prevista,
        status="ativo",
        valor_multa=0.0
    )
    
    exemplar.status = "emprestado"
    
    db.add(novo_emprestimo)
    db.commit()
    db.refresh(novo_emprestimo)
    
    return novo_emprestimo

def verificar_limite_emprestimos(db: Session, usuario_id: int) -> bool:
    usuario = db.query(User).filter(User.id == usuario_id).first()
    
    if not usuario:
        raise ValueError("usuário-nao-encontrado")
    
    limite = LIMITES_EMPRESTIMOS.get(usuario.tipo, 5)  
    
    if limite == -1:
        return True
    
    emprestimos_ativos = db.query(Emprestimo).filter(
        Emprestimo.usuario_id == usuario_id,
        Emprestimo.status == "ativo"  
    ).count()
    
    return emprestimos_ativos < limite

def obter_limite_usuario(tipo_usuario: str) -> int:
    return LIMITES_EMPRESTIMOS.get(tipo_usuario, 5)

def obter_emprestimos_ativos_usuario(db: Session, usuario_id: int) -> int:
    return db.query(Emprestimo).filter(
        Emprestimo.usuario_id == usuario_id,
        Emprestimo.status == "ativo"
    ).count()
    