from typing import Optional, Any
from datetime import datetime

def tipo_de_usuario(v: str) -> str:
    if v not in ["bibliotecario", "aluno", "professor"]:
        raise ValueError("Tipo de usuário inválido")
    return v.lower()

def status_usuario(v: str) -> str:
    if v not in ["ativo", "suspenso", "inativo"]:
        raise ValueError("Status de usuário inválido")
    
def validar_titulo(titulo: Any) -> str:
    if not isinstance(titulo, str):
        raise ValueError('Título deve ser uma string')
    
    titulo_limpo = titulo.strip()
    
    if not titulo_limpo:
        raise ValueError('Título do livro é obrigatório')
    
    if len(titulo_limpo) < 2:
        raise ValueError('Título deve ter pelo menos 2 caracteres')
    
    if len(titulo_limpo) > 200:
        raise ValueError('Título deve ter no máximo 200 caracteres')
    
    return titulo_limpo

def validar_autor(autor: Any) -> str:
    if not isinstance(autor, str):
        raise ValueError('Autor deve ser uma string')
    
    autor_limpo = autor.strip()
    
    if not autor_limpo:
        raise ValueError('Autor do livro é obrigatório')
    
    if len(autor_limpo) < 2:
        raise ValueError('Nome do autor deve ter pelo menos 2 caracteres')
    
    if len(autor_limpo) > 100:
        raise ValueError('Nome do autor deve ter no máximo 100 caracteres')
    
    if ' ' not in autor_limpo:
        raise ValueError('Informe o nome completo do autor (nome e sobrenome)')
    
    if any(char.isdigit() for char in autor_limpo):
        raise ValueError('Nome do autor não pode conter números')
    
    return autor_limpo

def validar_ano_publicacao(ano: Any) -> Optional[int]:
    if ano is None:
        return None
    
    try:
        ano_int = int(ano)
    except (ValueError, TypeError):
        raise ValueError('Ano de publicação deve ser um número válido')
    
    ano_atual = datetime.now().year
    
    if ano_int < 1000:
        raise ValueError('Ano de publicação deve ser maior que 1000')
    
    if ano_int > ano_atual:
        raise ValueError(f'Ano de publicação inválido (ano atual: {ano_atual})')
    
    return ano_int