from sqlalchemy import String, Date, DateTime, UniqueConstraint, ForeignKey, Integer, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.app.database import Base


class User(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("matricula", name="uq_usuarios_matricula"),
        UniqueConstraint("email", name="uq_usuarios_email"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    matricula: Mapped[str] = mapped_column(String(20), nullable=False, index=True, unique=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # atendente, aluno, professor, tecnico
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ativo", index=True)  # ativo, suspenso, inativo
    motivo_suspensao: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    emprestimos: Mapped[list["Emprestimo"]] = relationship(
        back_populates="usuario", 
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
#     reservas: Mapped[list["Reserva"]] = relationship(
#         back_populates="usuario",
#         cascade="all, delete-orphan", 
#         passive_deletes=True,
#     )
#     multas: Mapped[list["Multa"]] = relationship(
#         back_populates="usuario",
#         cascade="all, delete-orphan",
#         passive_deletes=True,
#     )

class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    autor: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    ano_publicacao: Mapped[int | None] = mapped_column(nullable=True)
    editora: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sinopse: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    exemplares: Mapped[list["Exemplar"]] = relationship(
        back_populates="livro",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
#     reservas: Mapped[list["Reserva"]] = relationship(
#         back_populates="livro", 
#         cascade="all, delete-orphan",
#         passive_deletes=True,
#     )

class Exemplar(Base):
    __tablename__ = "exemplares"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_exemplares_codigo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
    livro_id: Mapped[int] = mapped_column(
        ForeignKey("livros.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="disponivel", index=True)  # disponivel, emprestado, manutencao, reservado
    data_aquisicao: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    livro: Mapped["Livro"] = relationship(back_populates="exemplares")
    emprestimos: Mapped[list["Emprestimo"]] = relationship(
        back_populates="exemplar",
        cascade="all, delete-orphan", 
        passive_deletes=True,
    )

class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    exemplar_id: Mapped[int] = mapped_column(
        ForeignKey("exemplares.id", ondelete="CASCADE"), 
        index=True,
        nullable=False,
    )
    data_emprestimo: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_devolucao_prevista: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_devolucao_real: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ativo", index=True)  # ativo, finalizado, atrasado, cancelado
    valor_multa: Mapped[float] = mapped_column(nullable=False, default=0.0)

    usuario: Mapped["User"] = relationship(back_populates="emprestimos")
    exemplar: Mapped["Exemplar"] = relationship(back_populates="emprestimos")
    # multas: Mapped[list["Multa"]] = relationship(
    #     back_populates="emprestimo",
    #     cascade="all, delete-orphan",
    #     passive_deletes=True,
    # )

# # -----------------------------
# # Reserva
# # -----------------------------
# class Reserva(Base):
#     __tablename__ = "reservas"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     usuario_id: Mapped[int] = mapped_column(
#         ForeignKey("usuarios.id", ondelete="CASCADE"),
#         index=True,
#         nullable=False,
#     )
#     livro_id: Mapped[int] = mapped_column(
#         ForeignKey("livros.id", ondelete="CASCADE"),
#         index=True, 
#         nullable=False,
#     )
#     data_reserva: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     data_expiracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
#     status: Mapped[str] = mapped_column(String(20), nullable=False, default="pendente", index=True)  # pendente, ativa, cancelada, expirada, concluida

#     usuario: Mapped["User"] = relationship(back_populates="reservas")
#     livro: Mapped["Livro"] = relationship(back_populates="reservas")
