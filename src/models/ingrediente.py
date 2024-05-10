from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
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
