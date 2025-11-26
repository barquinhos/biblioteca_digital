from pydantic import BaseModel, Field
from typing import Optional

class ExemplarBase(BaseModel):
    livro_id: int = Field(..., description="ID do livro")

class ExemplarCreate(ExemplarBase):
    pass

class ExemplarOut(ExemplarBase):
    id: int = Field(..., description="ID do exemplar")
    codigo: str = Field(..., description="Código único do exemplar")
    status: str = Field(..., description="Status: disponivel, emprestado, manutencao")
    
    class Config:
        from_attributes = True