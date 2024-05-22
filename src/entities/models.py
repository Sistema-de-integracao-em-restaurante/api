from typing import List
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    String,
    Integer,
    DateTime,
    func,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    mapped_column,
    Mapped,
)
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class IngredientePrato(Base):
    __tablename__ = "ingrediente_prato"

    id_ingrediente: Mapped[int] = mapped_column(
        ForeignKey("ingrediente.id"), primary_key=True
    )
    id_prato: Mapped[int] = mapped_column(
        ForeignKey("prato.id"), primary_key=True
    )
    quantidade_ingrediente = Column(Integer, nullable=False)
    ingrediente: Mapped["Ingrediente"] = relationship()
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
            "id_ingrediente": self.id_ingrediente,
            "id_prato": self.id_prato,
            "quantidade_ingrediente": self.quantidade_ingrediente,
            "ingrediente": (
                self.ingrediente.serialize()
                if self.ingrediente is not None
                else {}
            ),
            "created_at": self.created_at,
        }


class Ingrediente(Base):
    __tablename__ = "ingrediente"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(Integer)
    medida = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "medida": self.medida,
            "created_at": self.created_at,
        }


class Prato(Base):
    __tablename__ = "prato"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    ingredientes: Mapped[List["IngredientePrato"]] = relationship()
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "ingredientes": [i.serialize() for i in self.ingredientes],
            "created_at": self.created_at,
        }


class PratoPedido(Base):
    __tablename__ = "prato_pedido"

    id_prato: Mapped[int] = mapped_column(
        ForeignKey("prato.id"), primary_key=True
    )
    id_pedido: Mapped[int] = mapped_column(
        ForeignKey("pedido.id"), primary_key=True
    )
    quantidade_prato = Column(Integer, nullable=False)
    prato: Mapped["Prato"] = relationship()
    created_at = Column(DateTime, default=func.now())

    @hybrid_property
    def preco_total(self):
        if not self.prato:
            return 0
        return round(self.prato.preco * self.quantidade_prato, 2)

    def serialize(self):
        return {
            "id_prato": self.id_prato,
            "id_pedido": self.id_pedido,
            "quantidade_prato": self.quantidade_prato,
            "prato": self.prato.serialize() if self.prato is not None else {},
            "preco_total": self.preco_total,
            "created_at": self.created_at,
        }


class Pedido(Base):
    __tablename__ = "pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_cliente = Column(String, nullable=False)
    forma_pagamento = Column(String, nullable=False)
    pratos: Mapped[List["PratoPedido"]] = relationship()
    created_at = Column(DateTime, default=func.now())

    @hybrid_property
    def preco_total_pedido(self):
        return round(sum(acc.preco_total for acc in self.pratos), 2)

    def serialize(self):
        return {
            "id": self.id,
            "nome_cliente": self.nome_cliente,
            "forma_pagamento": self.forma_pagamento,
            "pratos": [p.serialize() for p in self.pratos],
            "preco_total_pedido": self.preco_total_pedido,
            "created_at": self.created_at,
        }
