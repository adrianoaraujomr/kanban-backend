import os
import requests
import logging
import json

from typing import List
from flask import abort

from src.integrations.github.dto.issue_dto import GithubIssueDto, UpdateGithubIssueDto

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
        response = requests.post(f"{github_url}/repos/{owner}/{repository}/issues", json=issue, headers=headers)
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
    
def get_issue_from_repo(owner, repository, issue_number) -> GithubIssueDto:
    if not owner or not repository or not issue_number:
        abort(400, "Owner and Repository and Issue Number name must be passed")

    try:
        response = requests.get(f"{github_url}/repos/{owner}/{repository}/issues/{issue_number}", headers=headers)
        response.raise_for_status()
        body = response.json()
        return GithubIssueDto(body)
    except requests.exceptions.HTTPError as http_error:
        logging.error(f"HTTP error ocurred: {http_error}")
        raise http_error
    except Exception as error:
        logging.error(f"An error ocurred during request: {error}")
        raise error
    


def update_issue(owner, repository, issue_number, data) -> GithubIssueDto:
    if not owner or not repository or not issue_number:
        abort(400, "Owner and Repository and Issue Number name must be passed")
        
    try:
        request_body = UpdateGithubIssueDto(data).__dict__
        response = requests.patch(f"{github_url}/repos/{owner}/{repository}/issues/{issue_number}", json=request_body, headers=headers)
        response.raise_for_status()
        body = response.json()
        return GithubIssueDto(body)
    except requests.exceptions.HTTPError as http_error:
        logging.error(f"HTTP error ocurred: {http_error}")
        raise http_error
    except Exception as error:
        logging.error(f"An error ocurred during request: {error}")
        raise error

def lock_issue(owner, repository, issue_number, lock_reason) -> bool:
    if not owner or not repository or not issue_number:
        abort(400, "Owner and Repository and Issue Number name must be passed")
    
    if not lock_reason:
        abort(400, "A lock reason must be provided")

    try:    
        request_body = {"lock_reason": lock_reason}
        response = requests.put(f"{github_url}/repos/{owner}/{repository}/issues/{issue_number}/lock", headers=headers, json=request_body)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as http_error:
        logging.error(f"HTTP error ocurred: {http_error}")
        raise http_error
    except Exception as error:
        logging.error(f"An error ocurred during request: {error}")
        raise error
