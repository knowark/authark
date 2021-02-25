from marshmallow import Schema, fields


class EntitySchema(Schema):
    id = fields.Str(
        metadata=dict(example="f52706c8-ac08-4f9d-a092-8038d1769825"))
    created_at = fields.Int(
        data_key='createdAt', dump_only=True,
        metadata=dict(example="1558580890"))
    created_by = fields.Str(
        data_key='createdBy', dump_only=True,
        metadata=dict(example="cc14f686-d978-42ef-b5a7-1347716aac37"))
    updated_at = fields.Int(
        data_key='updatedAt', dump_only=True,
        metadata=dict(example="1558580890"))
    updated_by = fields.Str(
        data_key='updatedBy', dump_only=True,
        metadata=dict(example="cc14f686-d978-42ef-b5a7-1347716aac37"))
