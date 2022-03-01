from marshmallow import (
    Schema,
    fields,
)
from marshmallow.validate import (
    Length,
    Range,
)


class StockSchema(Schema):
    symbol = fields.Str(required=True, validate=Length(min=1, max=10))
    name = fields.Str(required=True, validate=Length(min=1, max=50))
    price = fields.Float(required=True, validate=Range(min=1))
    quantity = fields.Int(required=True, validate=Range(min=1))


class StocksSchema(Schema):
    stocks = fields.Nested(nested=StockSchema, required=True, many=True)
