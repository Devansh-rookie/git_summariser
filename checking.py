import json
import requests 
from dotenv import load_dotenv

load_dotenv()


# At the top we can construct the request we want to make 
GITHUB_BASE_URL = 'https://api.github.com' 
repo = 'noterAI' 
owner = "Himasnhu-AT"
url = f"{GITHUB_BASE_URL}/repos/{owner}/{repo}"

token = ""

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

def bprint(repo):
    with open("some.json", 'w') as f:
        json.dump(repo, f)

if response.status_code == 200:
    repo_data = response.json()
    print(f"Repository Name: {repo_data['name']}")
    print(f"Description: {repo_data['description']}")
    print(f"Stars: {repo_data['stargazers_count']}")
    print(f"Forks: {repo_data['forks_count']}")
    # print(repo_data)
    bprint(repo_data)
else:
    print(f"Failed to fetch data: {response.status_code}")