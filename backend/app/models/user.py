from typing_extensions import Annotated
from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from pydantic.config import ConfigDict
from pydantic.functional_validators import BeforeValidator

from backend.app.utils.validators import tipo_de_usuario

EmailLower = Annotated[EmailStr, BeforeValidator(lambda v: str(v).lower())]
TipoUser = Annotated[str, BeforeValidator(tipo_de_usuario)]
# StatusUser = Annotated[str, BeforeValidator(status_usuario)]

class UserBase(BaseModel):
    id: int
    nome: str
    matricula: str
    email: EmailLower
    tipo: TipoUser  
    # status: StatusUser 

class UserCreate(UserBase):
    senha: str = Field(..., min_length=6, max_length=72)

class UserLogin(BaseModel):
    email: EmailLower
    senha: str = Field(..., min_length=6, max_length=72)
    
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