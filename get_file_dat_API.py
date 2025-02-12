import requests
import json
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

# GitHub API endpoint
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
MAX_SIZE_IN_KB = 50
# Your GitHub Personal Access Token
# GITHUB_TOKEN = os.getenv("GIT_TOKEN")
#

GITHUB_TOKEN = os.getenv("GIT_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Please set the GIT_TOKEN environment variable.")


# Define the GraphQL query
query = """
query ($owner: String!, $repo: String!, $expression: String!) {
  repository(owner: $owner, name: $repo) {
    object(expression: $expression) {
      ... on Tree {
        entries {
          name
          type
          object {
            ... on Blob {
              text
              byteSize
            }
            ... on Tree {
              entries {
                name
                type
                object {
                  ... on Blob {
                    text
                    byteSize
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

headers = {"Authorization": f"token {GITHUB_TOKEN}"}


def fetch_repo_contents(owner, repo, expression):
    """
    Recursively fetches all files in a GitHub repository.
    """
    # headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    variables = {"owner": owner, "repo": repo, "expression": expression}
    response = requests.post(
        GITHUB_GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code}, {response.text}")

    data = response.json()
    entries = data["data"]["repository"]["object"]["entries"]
    files = {}

    for entry in entries:
        #  and entry["object"]["byteSize"] < 1000
        if entry["type"] == "blob" and entry["object"]["byteSize"] < MAX_SIZE_IN_KB*1024:
            # It's a file, get its content
            files[entry["name"]] = entry.get("object", {}).get("text", None)
        elif entry["type"] == "tree":
            # It's a directory, recursively fetch its contents
            sub_expression = f"{expression}{entry['name']}/"
            sub_files = fetch_repo_contents(owner, repo, sub_expression)
            files.update({f"{entry['name']}/{k}": v for k, v in sub_files.items()})

    return files

# Example usage
owner = "Devansh-rookie"  # Replace with the repo owner username
repo = "CSES"         # Replace with the repository name
branch = "main"            # Replace with the branch name

app = FastAPI()
try:
    all_files = fetch_repo_contents(owner, repo, f"{branch}:")
    # for file_path, content in all_files.items():
        # print(f"File: {
        # file_path}")
        # print(f"Content: {content[:100]}...")  # Print the first 100 characters of content
    with open("files_data.json", 'w') as f:
        json.dump(all_files, f)
    print(all_files)
    # with open("checking_new.json", 'w') as f:
    #     json.dump(all_files, f)
    app = FastAPI()

    @app.get("/get_file_data")
    async def get_file_data():
        return all_files
except Exception as e:
    print(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
