from typing import List
from sqlalchemy import Column, Float, ForeignKey, String, Integer, DateTime, \
     func
from sqlalchemy.orm import declarative_base, relationship, mapped_column, \
     Mapped

Base = declarative_base()


class IngredientePrato(Base):
    __tablename__ = 'ingrediente_prato'

    id_ingrediente: Mapped[int] = mapped_column(ForeignKey("ingrediente.id"),
                                                primary_key=True)
    id_prato: Mapped[int] = mapped_column(ForeignKey("prato.id"),
                                          primary_key=True)
    quantidade_ingrediente = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
                'id_ingrediente': self.id_ingrediente,
                'id_prato': self.id_prato,
                'quantidade_ingrediente': self.quantidade_ingrediente,
                'created_at': self.created_at
        }


class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
                'id': self.id,
                'nome': self.nome,
                'descricao': self.descricao,
                'created_at': self.created_at
        }


class Prato(Base):
    __tablename__ = 'prato'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    ingredientes: Mapped[List["IngredientePrato"]] = relationship()
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
                'id': self.id,
                'nome': self.nome,
                'preco': self.preco,
                'created_at': self.created_at,
                'ingredientes': [i.serialize() for i in self.ingredientes]
        }
