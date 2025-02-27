import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

directory = "results"
if not os.path.exists(directory):
    os.mkdir(directory)


# GitHub API endpoint
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
MAX_SIZE_IN_KB = 25
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
    # """
    # Recursively fetches all files in a GitHub repository.
    # """
    # # headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    # variables = {"owner": owner, "repo": repo, "expression": expression}
    # response = requests.post(
    #     GITHUB_GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers
    # )

    # if response.status_code != 200:
    #     raise Exception(f"Query failed: {response.status_code}, {response.text}")

    # data = response.json()
    # entries = data["data"]["repository"]["object"]["entries"]
    # files = {}
    #
    #



    """Recursively fetch files with path validation"""
    # Split expression into branch and path
    if ":" in expression:
        branch, path = expression.split(":", 1)
    else:
        branch = expression
        path = ""

    # Verify branch exists using REST API
    branch_url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    branch_res = requests.get(branch_url, headers=headers)
    if branch_res.status_code != 200:
        # available = list_branches(owner, repo)
        raise Exception(f"Branch '{branch}' not found. Available: {', '.join('.')}")

    # Verify path exists using REST API
    if path:
        path_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
        path_res = requests.get(path_url, headers=headers)
        if path_res.status_code != 200:
            raise Exception(f"Path '{path}' not found in branch '{branch}'")

    # Continue with GraphQL processing
    variables = {"owner": owner, "repo": repo, "expression": f"{branch}:{path}"}

    # variables = {"owner": owner, "repo": repo, "expression": expression}
    response = requests.post(
            GITHUB_GRAPHQL_URL,
            json={"query": query, "variables": variables},
            headers=headers
        )

    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code}, {response.text}")

    data = response.json()
    print(data)

    # Add comprehensive error checking
    if not data.get("data"):
        if "errors" in data:
            error_msg = "\n".join([e["message"] for e in data["errors"]])
            raise Exception(f"GraphQL errors: {error_msg}")
        raise Exception("No data in response")

    repo_data = data["data"].get("repository")
    if not repo_data:
        raise Exception("Repository not found or access denied")

    repo_object = repo_data.get("object")
    if not repo_object:
        raise Exception(f"Git reference '{expression}' not found")

    if "entries" not in repo_object:  # Handle non-tree objects
        if repo_object.get("type") == "blob":
            return {expression.split(":")[-1]: repo_object.get("text")}
        return {}

    entries = repo_object["entries"]
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


def fetch_repo_structure(owner, repo, branch):
    """
    Fetch the structure of a repository.
    """
    tree_data = get_repo_tree(owner, repo, branch)
    return print_directory_tree(tree_data)



if __name__ == "__main__":

    owner = "Devansh-rookie"  # Replace with the repo owner username
    repo = "git_summariser"         # Replace with the repository name
    branch = "main"            # Replace with the branch name
    try:
        all_files = fetch_repo_contents(owner, repo, f"{branch}:")

        with open("results/files_data.json", 'w') as f:
            json.dump(all_files, f)

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
        with open("results/tree_struct.txt", 'w') as f:
            f.write(fetch_repo_structure(owner, repo, branch))

    except Exception as e:
        print(e)
        print("e in tree")
