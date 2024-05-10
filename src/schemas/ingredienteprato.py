from marshmallow import Schema, fields


class IngredientePratoCreationSchema(Schema):
    id_ingrediente = \
        fields.Integer(required=True,
                       error_messages={"required":
                                       "ID do ingrediente e obrigatorio"})
    quantidade_ingrediente = \
        fields.Integer(required=True,
                       error_messages={"required":
                                       "Quantidade ingrediente e obrigatorio"})
