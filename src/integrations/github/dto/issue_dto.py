from src.integrations.github.enum.issue_state import IssueState, IssueStateReason

class GithubIssueDto:
  def __init__(self, kwargs) -> None:
    self.id = kwargs["id"]
    self.url = kwargs["url"]
    self.repository_url = kwargs["repository_url"]
    self.state = kwargs["state"]
    self.body = kwargs["body"]
    self.number = kwargs["number"]
    self.closed_at = kwargs["closed_at"]
    self.created_at = kwargs["created_at"]
    self.updated_at = kwargs["updated_at"]

  def __eq__(self, other) -> bool:
    return self.id == other.id
  
class CreateGithubIssueDto:
  def __init__(self, kwargs) -> None:
    self.title = kwargs["title"] # Obrigatorio
    self.body = kwargs["body"]
    self.assignee = kwargs["assignee"]
    self.type = kwargs["type"]

class UpdateGithubIssueDto:
  def __init__(self, kwargs) -> None:
    if "title" in kwargs.keys():
      self.title = kwargs["title"]
    if "body" in kwargs.keys():
      self.body = kwargs["body"]
    if "assignee" in kwargs.keys():
      self.assignee = kwargs["assignee"]
    if "type" in kwargs.keys():
      self.type = kwargs["type"]
    if "state" in kwargs.keys():
      self.state = IssueState[kwargs["state"]]
    if "state_reason" in kwargs.keys():
      self.state_reason = IssueStateReason[kwargs["state_reason"]]
