import os
import requests
import logging

from typing import List
from flask import abort

from src.integrations.github.dto.issue_dto import GithubIssueDto

github_url = os.getenv("GITHUB_API_URL")
github_token = os.getenv("GITHUB_API_TOKEN")

headers = {
    "Accept": "application/vnd.github.text-match+json",
    "Authorization": f"Bearer {github_token}"
}

def create_issue(owner, repository, issue) -> GithubIssueDto:
    if not owner or not repository:
        abort(400, "Owner and Repository name must be passed")
    
    try:
        response = requests.post(f"{github_url}/repos/{owner}/{repository}/issues", data=issue, headers=headers)
        response.raise_for_status()
        body = response.json()
        return GithubIssueDto(body)
    except requests.exceptions.HTTPError as http_error:
        logging.error(f"HTTP error ocurred: {http_error}")
        raise http_error
    except Exception as error:
        logging.error(f"An error ocurred during request: {error}")
        raise error


def get_issues_from_repo(owner, repository) -> List[GithubIssueDto]:
    if not owner or not repository:
        abort(400, "Owner and Repository name must be passed")

    try:
        response = requests.get(f"{github_url}/repos/{owner}/{repository}/issues", headers=headers)
        response.raise_for_status()
        body = response.json()
        return [GithubIssueDto(issue) for issue in body]
    except requests.exceptions.HTTPError as http_error:
        logging.error(f"HTTP error ocurred: {http_error}")
        raise http_error
    except Exception as error:
        logging.error(f"An error ocurred during request: {error}")
        raise error
        
