class GithubIssueDto:
  def __init__(self, kwargs) -> None:
    self.id = kwargs["id"]
    self.url = kwargs["url"]
    self.repository_url = kwargs["repository_url"]
    self.state = kwargs["state"]
    self.body = kwargs["body"]
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