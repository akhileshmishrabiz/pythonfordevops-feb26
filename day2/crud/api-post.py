import requests
from dotenv import load_dotenv
import os

# create a github repo -> post req
# authentication -> PAT , Authrizatrion to create the repo
#
load_dotenv()

PAT = os.getenv("PAT")
repo_to_create_for_demo = "pythonfordevops-crud-operations"

github_user = "akhileshmishrabiz"
# url = f"https://api.github.com/{github_user}/repos"


def create_github_repo(pat, repo_name):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "name": repo_name,
        "description": "This is your demo repo!",
        "private": False,
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def delete_github_repo(pat, repo_name):
    url = f"https://api.github.com/repos/{github_user}/{repo_name}"
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.delete(url, headers=headers)
    return response.status_code

# Example usage
if __name__ == "__main__":
    # Create the repo
    # repo_response = create_github_repo(PAT, repo_to_create_for_demo)
    # print(repo_response)

    # delete the repo

    response = delete_github_repo(PAT, repo_to_create_for_demo)
    print(response)

