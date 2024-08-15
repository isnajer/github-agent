import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {"Authorization": f"Bearer {github_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed with status code:", response.status_code)
        return []

    return data

def fetch_issue_comments(owner, repo, issue_number):
    return fetch_github(owner, repo, f"issues/{issue_number}/comments")

def fetch_github_issues(owner, repo):
    issues = fetch_github(owner, repo, "issues")
    return load_issues(owner, repo, issues)

def load_issues(owner, repo, issues):
    docs = []
    for entry in issues:
        issue_number = entry["number"]
        comments = fetch_issue_comments(owner, repo, issue_number)
        
        metadata = {
            "author": entry["user"]["login"],
            "comments_count": entry["comments"],
            "labels": [label["name"] for label in entry["labels"]],
            "created_at": entry["created_at"],
            "issue_number": issue_number,
            "title": entry["title"],
        }
        
        content = f"Issue #{issue_number}: {entry['title']}\n\nDescription:\n{entry['body']}\n\nComments:\n"
        for comment in comments:
            content += f"- {comment['user']['login']}: {comment['body']}\n"
        
        doc = Document(page_content=content, metadata=metadata)
        docs.append(doc)
        
        print(f"Fetched issue #{issue_number}:")
        print(content)
        print("-" * 50)

    return docs

# You can keep the print statement in fetch_github if you want to see the raw API response
# def fetch_github(owner, repo, endpoint):
#     ...
    print(data)
    return data