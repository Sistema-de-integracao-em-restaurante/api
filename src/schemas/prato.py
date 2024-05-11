from marshmallow import Schema, fields


class PratoCreationSchema(Schema):
    nome = fields.String(required=True,
                         error_messages={"required": "Nome e obrigatorio"})
    preco = fields.Float(required=True,
                         error_messages={"required": "Preco e obrigatorio"})
