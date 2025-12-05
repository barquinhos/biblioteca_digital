from typing_extensions import Annotated
from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from pydantic.config import ConfigDict
from pydantic.functional_validators import BeforeValidator

from backend.app.utils.validators import tipo_de_usuario

EmailLower = Annotated[EmailStr, BeforeValidator(lambda v: str(v).lower())]
TipoUser = Annotated[str, BeforeValidator(tipo_de_usuario)]

class UserBase(BaseModel):
    id: int
    nome: str
    matricula: str
    email: EmailLower
    tipo: TipoUser  

class UserCreate(UserBase):
    senha: str = Field(..., min_length=6, max_length=72)

class UserLogin(BaseModel):
    email: EmailLower
    senha: str = Field(..., min_length=6, max_length=72)

class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    tipo: Optional[str] = Field(None, description="Tipo: aluno, professor, bibliotecario")
    
    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: Optional[int] = None
    email: EmailLower
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenWithUser(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut