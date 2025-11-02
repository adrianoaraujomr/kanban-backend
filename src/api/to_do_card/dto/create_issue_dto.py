from marshmallow import Schema, fields 

class CreateIssueDto(Schema):
    """
    """
    title = fields.Str(required=True)
    body = fields.Str(required=False)
    assignee = fields.Str(required=False)
    type = fields.Str(required=False)