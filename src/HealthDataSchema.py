from marshmallow import Schema, fields, validate

class HealthDataSchema(Schema):
    heart_rate = fields.Integer(required=True, validate=validate.Range(min=40, max=200))
    blood_pressure = fields.Str(required=True, validate=validate.Regexp(r'^\d{1,3}/\d{1,3}$'))
    temperature = fields.Float(required=True, validate=validate.Range(min=35.0, max=42.0))
