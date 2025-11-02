from src.integrations.github.enum.issue_state import IssueState, IssueStateReason
from marshmallow import Schema, fields 

class CreateIssueDto(Schema):
    """
    """
    title = fields.Str(required=True)
    body = fields.Str(required=False)
    type = fields.Str(required=False)
    assignee = fields.Str(required=False)

class UpdateIssueDto(Schema):
    """
    """
    title = fields.Str(required=False)
    body = fields.Str(required=False)
    type = fields.Str(required=False)
    assignee = fields.Str(required=False)
    state = fields.Enum(required=False, enum=IssueState)
    state_reason = fields.Enum(required=False, enum=IssueStateReason)
