from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmprestimoBase(BaseModel):
    usuario_id: int = Field(..., description="ID do usuário")
    exemplar_id: int = Field(..., description="ID do exemplar") # verificar
    data_devolucao_prevista: datetime = Field(..., description="Data prevista para devolução")

class EmprestimoCreate(EmprestimoBase):
    pass

class EmprestimoOut(EmprestimoBase):
    id: int = Field(..., description="ID do empréstimo")
    data_emprestimo: datetime = Field(..., description="Data do empréstimo")
    data_devolucao_real: Optional[datetime] = Field(None, description="Data real da devolução")
    status: str = Field(..., description="Status: ativo, finalizado, atrasado")
    valor_multa: float = Field(..., description="Valor da multa")
    
    class Config:
        from_attributes = True