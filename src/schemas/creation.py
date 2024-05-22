from marshmallow import Schema, fields


class IngredienteCreationSchema(Schema):
    nome = fields.String(
        required=True, error_messages={"required": "Nome e obrigatorio"}
    )
    descricao = fields.String(required=False, load_default=None)


class IngredientePratoCreationSchema(Schema):
    id_ingrediente = fields.Integer(
        required=True, error_messages={"required": "ID do ingrediente e obrigatorio"}
    )
    quantidade_ingrediente = fields.Integer(
        required=True,
        error_messages={"required": "Quantidade ingrediente e obrigatorio"},
    )


class PratoCreationSchema(Schema):
    nome = fields.String(
        required=True, error_messages={"required": "Nome e obrigatorio"}
    )
    preco = fields.Float(
        required=True, error_messages={"required": "Preco e obrigatorio"}
    )


class PedidoCreationSchema(Schema):
    nome_cliente = fields.String(
        required=True, error_messages={"required": "Nome do cliente e obrigatorio"}
    )
    forma_pagamento = fields.String(
        required=True,
        validate=lambda fp: fp in ["Dinheiro", "Credito", "Debito"],
        error_messages={
            "required": "Forma de pagamento e obrigatorio",
            "validator_failed": "Apenas as opcoes: 'Dinheiro'"
            ", 'Credito' e 'Debito' estao disponíveis",
        },
    )


class PratoPedidoCreationSchema(Schema):
    id_prato = fields.Integer(
        required=True, error_messages={"required": "ID do pedido e obrigatorio"}
    )
    quantidade_prato = fields.Integer(
        required=True, error_messages={"required": "Quantidade pedido e obrigatorio"}
    )
