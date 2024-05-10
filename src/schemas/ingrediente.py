from marshmallow import Schema, fields


class IngredienteCreationSchema(Schema):
    nome = fields.String(required=True,
                         error_messages={"required": "Nome e obrigatorio"})
    descricao = fields.String(required=False,
                              load_default=None)
