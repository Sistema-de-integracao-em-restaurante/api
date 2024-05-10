from sqlalchemy import Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import declarative_base, relationship
from models.ingrediente_prato import IngredientePrato

Base = declarative_base()


class Prato(Base):
    __tablename__ = 'prato'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float)
    ingredientes = relationship('ingrediente', secondary=IngredientePrato,
                                back_populates='pratos')
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
                'id': self.id,
                'nome': self.nome,
                'preco': self.preco,
                'created_at': self.created_at
        }
