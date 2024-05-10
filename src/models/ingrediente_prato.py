from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class IngredientePrato(Base):
    __tablename__ = 'ingrediente_prato'

    # idIngrediente = Column(Integer, ForeignKey('ingrediente.id'),
    #                        primary_key=True)
    # idPrato = Column(Integer, ForeignKey('prato.id'),
    #                  primary_key=True)
    # quantidadeIngrediente = Column(Integer, nullable=False)
    # created_at = Column(DateTime, default=func.now())

    idIngrediente: Mapped[int] = mapped_column(ForeignKey("ingrediente.id"),
                                               primary_key=True)
    idPrato: Mapped[int] = mapped_column(ForeignKey("prato.id"),
                                         primary_key=True)
    quantidadeIngrediente = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def serialize(self):
        return {
                'idIngrediente': self.idIngrediente,
                'idPrato': self.idPrato,
                'quantidadeIngreiente': self.quantidadeIngrediente,
                'created_at': self.created_at
        }
