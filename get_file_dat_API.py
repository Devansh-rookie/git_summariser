import requests
import json
import os
from fastapi import FastAPI
from dotenv import load_dotenv

runAPI = False

load_dotenv()

directory = "results"
if not os.path.exists(directory):
    os.mkdir(directory)


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

num_of_folders = 0

def fetch_repo_details(owner, repo):
    basic = ""
    # Endpoint to fetch basic repo details
    repo_url = f'https://api.github.com/repos/{owner}/{repo}'
    repo_response = requests.get(repo_url, headers=headers)
    if repo_response.ok:
        repo_data = repo_response.json()
        stars = repo_data.get('stargazers_count')
        forks = repo_data.get('forks_count')
        issues = repo_data.get('open_issues_count')
        watchers = repo_data.get('watchers_count')
        description = repo_data.get('description')
        basic += ("Repository Details:") +'\n'
        basic += (f"  Description: {description}") +'\n'
        basic += (f"  Stars: {stars}") +'\n'
        basic += (f"  Forks: {forks}") +'\n'
        basic += (f"  Open Issues: {issues}") +'\n'
        basic += (f"  Watchers: {watchers}") + '\n'

    else:
        print("Failed to fetch repository details")
        return None

    # Endpoint to fetch branches
    branches_url = f'https://api.github.com/repos/{owner}/{repo}/branches'
    branches_response = requests.get(branches_url, headers=headers)
    if branches_response.ok:
        branches_data = branches_response.json()
        branch_names = [branch.get('name') for branch in branches_data]
        basic += ("\nBranches:\n")
        for name in branch_names:
            basic += (f"  {name}\n")
    else:
        print("Failed to fetch branches")

    return basic


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



def get_repo_tree(owner, repo, branch="main"):

    # Step 1: Get branch details to retrieve tree SHA
    branch_url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    branch_response = requests.get(branch_url, headers=headers)
    if not branch_response.ok:
        raise Exception("Failed to fetch branch details")
    branch_data = branch_response.json()
    tree_sha = branch_data["commit"]["commit"]["tree"]["sha"]

    # Step 2: Fetch the recursive tree structure
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1"
    tree_response = requests.get(tree_url, headers=headers)
    if not tree_response.ok:
        raise Exception("Failed to fetch repository tree")
    tree_data = tree_response.json()

    return tree_data


def print_directory_tree(tree_data):
    """
    Process and print a simple text-based tree structure.
    """
    # Build a hierarchical dictionary from the flat list of tree entries.

    structure = ""
    tree = {}
    for item in tree_data.get("tree", []):
        parts = item["path"].split("/")
        current = tree
        for part in parts:
            current = current.setdefault(part, {})
    def build_tree(subtree, prefix=""):
        lines = []
        for key, nested in sorted(subtree.items()):
            lines.append(prefix + "|-- " + key)
            lines.extend(build_tree(nested, prefix + "    "))
        return lines
    structure = build_tree(tree)
    return "\n".join(structure)


# Example usage
owner = "Devansh-rookie"  # Replace with the repo owner username
repo = "git_summariser"         # Replace with the repository name
branch = "main"            # Replace with the branch name

if(runAPI):
    app = FastAPI()
try:
    all_files = fetch_repo_contents(owner, repo, f"{branch}:")
    # for file_path, content in all_files.items():
        # print(f"File: {
        # file_path}")
        # print(f"Content: {content[:100]}...")  # Print the first 100 characters of content
    with open("results/files_data.json", 'w') as f:
        json.dump(all_files, f)
    # print(all_files)
    # with open("checking_new.json", 'w') as f:
    #     json.dump(all_files, f)

    if(runAPI):
        app = FastAPI()

        @app.get("/get_file_data")
        async def get_file_data():
            return all_files
except Exception as e:
    print(e)


try:
    basic_details = fetch_repo_details(owner= owner, repo= repo)
    if(basic_details is None):
        print("can't fetch details.")
    else:
        with open("results/basic_details.txt", 'w') as f:
            f.write(basic_details)

except Exception as e:
    print(e)


try:
    tree_data = get_repo_tree(owner, repo, branch)
    treee = print_directory_tree(tree_data)
    with open("results/tree_struct.txt", 'w') as f:
        f.write(treee)

except Exception as e:
    print(e)
    print("e in tree")

if __name__ == "__main__" and runAPI:
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
