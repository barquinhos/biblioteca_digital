from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import Base, engine
from backend.app.routers import auth, auth_livro, emprestimo, exemplar

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI() 

origins = [
    "http://localhost:3000",   # Frontend web em React
    "http://10.0.2.2:8081",    # Emulador Android acessando sua máquina
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # quem pode acessar
    allow_credentials=True,
    allow_methods=["*"],        # métodos HTTP liberados: GET, POST, PUT, DELETE
    allow_headers=["*"],        # headers permitidos    
)

app.include_router(auth.router) 
app.include_router(auth_livro.router)
app.include_router(emprestimo.router)
app.include_router(exemplar.router)