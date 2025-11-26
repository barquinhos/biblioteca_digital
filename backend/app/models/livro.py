from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing_extensions import Annotated

from pydantic.config import ConfigDict
from pydantic.functional_validators import BeforeValidator

def validar_titulo(titulo: str) -> str:
    if len(titulo) < 2:
        raise ValueError('Título deve ter pelo menos 2 caracteres')
    return titulo

def validar_autor(autor: str) -> str:
    if len(autor) < 2:
        raise ValueError('Autor deve ter pelo menos 2 caracteres')
    return autor

def validar_ano_publicacao(ano: Optional[int]) -> Optional[int]:
    if ano and ano > datetime.now().year:
        raise ValueError('Ano de publicação não pode ser no futuro')
    return ano

TituloCanon = Annotated[str, BeforeValidator(validar_titulo)]
AutorCanon = Annotated[str, BeforeValidator(validar_autor)]
AnoPublicacaoCanon = Annotated[Optional[int], BeforeValidator(validar_ano_publicacao)]

class LivroBase(BaseModel):
    titulo: TituloCanon = Field(..., min_length=2, max_length=200, description="Título do livro")
    autor: AutorCanon = Field(..., min_length=2, max_length=100, description="Autor do livro")
    ano_publicacao: AnoPublicacaoCanon = Field(None, ge=1000, le=datetime.now().year, description="Ano de publicação")
    editora: Optional[str] = Field(None, max_length=100, description="Editora do livro")
    sinopse: Optional[str] = Field(None, max_length=2000, description="Sinopse do livro")
    data_cadastro: Optional[datetime] = Field(None, description="Data de cadastro no sistema")


class LivroCreate(LivroBase): 
    pass

class LivroUpdate(BaseModel):
    titulo: Optional[TituloCanon] = Field(None, min_length=2, max_length=200)
    autor: Optional[AutorCanon] = Field(None, min_length=2, max_length=100)
    ano_publicacao: Optional[AnoPublicacaoCanon] = Field(None, ge=1000, le=datetime.now().year)
    editora: Optional[str] = Field(None, max_length=100)
    sinopse: Optional[str] = Field(None, max_length=2000)

class LivroOut(LivroBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., ge=1, description="ID do livro")
    data_cadastro: datetime = Field(..., description="Data de cadastro no sistema")

class QuantidadeExemplaresOut(BaseModel):
    livro_id: int = Field(..., description="ID do livro")
    titulo: str = Field(..., description="Título do livro")
    autor: str = Field(..., description="Autor do livro")
    total_exemplares: int = Field(..., description="Total de exemplares")
    disponiveis: int = Field(..., description="Exemplares disponíveis")
    emprestados: int = Field(..., description="Exemplares emprestados")
    manutencao: int = Field(..., description="Exemplares em manutenção")
    
    class Config:
        from_attributes = True