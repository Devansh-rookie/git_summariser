from fastapi import FastAPI, HTTPException
import json
import os
import logging
from get_file_dat_API import fetch_repo_contents, fetch_repo_details, fetch_repo_structure
from try_summarize import get_dependencies, summarize_the_entire_thing, create_the_summaries
from variable_matching import findAllUsingGrep, findAllOccurrencesVariable
from get_file_types import fetch_file_types
import traceback
from fastapi.middleware.cors import CORSMiddleware
import re
app = FastAPI()
if os.path.exists("cache"):
    print("Cache directory exists")
else:
    os.makedirs("cache")

# Add CORS middleware
origins = [
    "http://localhost:5173",    # Vite default development port
    "http://localhost:3000",    # Alternative development port
    "https://git-summariser.vercel.app",  # Production frontend URL on Vercel
    "https://git-summariser-1.onrender.com",  # Production backend URL on Render
    "https://git-summariser.onrender.com"  # Alternative production URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Specific allowed origins
    allow_credentials=True,
    allow_methods=["*"],        # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],        # Allows all headers
)

async def get_combined_data_internal(owner: str, repo: str, branch: str):
    try:
        key_str = f'{owner}_{repo}_{branch}_fetch'

        if os.path.exists("cache/" + key_str + ".json"):
            with open("cache/" + key_str + ".json", "r") as f:
                return json.load(f)

        contents = fetch_repo_contents(owner, repo, branch)

        # Handle GitHub API errors first
        if isinstance(contents, dict) and 'message' in contents:
            raise HTTPException(502, detail=f"GitHub API Error: {contents['message']}")

        # Create directory if missing
        os.makedirs("results", exist_ok=True)

        with open("results/files_data.json", 'w') as f:
            json.dump(contents, f)


        fetch_dict = {
            "owner": owner,
            "repo": repo,
            "branch": branch,
            "data": [
                {"type": "Repository-Contents", "data": contents},
                {"type": "Repository-Detail", "data": fetch_repo_details(owner, repo)},
                {"type": "Repository-Structure", "data": fetch_repo_structure(owner, repo, branch)},
                {"type": "File-Types", "data": fetch_file_types()}
            ]
        }

        with open("cache/" + key_str + ".json", 'w') as f:
            json.dump(fetch_dict, f)

        return fetch_dict

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Data processing failed: {traceback.format_exc()}")
        raise HTTPException(500, detail=str(e))



"""Get combined repository data with dynamic parameters
Example request:
/api/fetch?owner=anushika1206&repo=virtual-air-hockey&branch=main
"""
@app.get("/api/fetch")
async def get_combined_data(
    owner: str = "octocat",
    repo: str = "Hello-World",
    branch: str = "master"
):
    try:
        return await get_combined_data_internal(owner, repo, branch)
    except Exception as e:
        raise HTTPException(500, detail=f"Error processing request: {str(e)}")


'''
[
    {
        "type": "repo_contents",
        "data": [...]
    },
    {
        "type": "repo_details",
        "data": {...}
    },
    {
        "type": "repo_structure",
        "data": {...}
    },
    {
        "type": "file_types",
        "data": {...}
    }
]

'''


@app.get("/api/summary")
async def get_repo_summary(
    owner: str = "octocat",
    repo: str = "Hello-World",
    branch: str = "master"
):
    """New endpoint that processes data from the existing endpoint"""
    try:
        key_str = f'{owner}_{repo}_{branch}_summary'

        if os.path.exists("cache/" + key_str + ".json"):
            with open("cache/" + key_str + ".json", "r") as f:
                return json.load(f)

        raw_data = await get_combined_data_internal(owner, repo, branch)

        data = raw_data['data'][0]['data']
        # print(raw_data)
        # print(data)
                # "owner_info": raw_data['data'][1]['data']['owner'],
        file_type_count = (raw_data['data'][3]['data'])
        if(file_type_count is not None):
            file_type_count = len(file_type_count)

        summary_dict = {
            "summary": {
                "Total-Files": len(raw_data['data'][0]['data']),
                "Number-Of-File-Types": file_type_count,
                "Project-Summary": summarize_the_entire_thing(data),
                "Filewise-Summary": create_the_summaries(data),
                "Dependencies": get_dependencies(data)
            },
            "metadata": {
                "repo": repo,
                "branch": branch,
            }
        }

        with open("cache/" + key_str + ".json", 'w') as f:
            json.dump(summary_dict, f)

        return summary_dict

    except Exception as e:
        raise HTTPException(500, detail=f"Summary generation failed: {str(e)}")


@app.get("/api/search")
async def search_codebase_string(
    owner: str = "octocat",
    repo: str = "Hello-World",
    branch: str = "master",
    query: str = ""):

    raw_data = await get_combined_data_internal(owner, repo, branch)
    data = raw_data['data'][0]['data']

    def search_codebase(code_data, search_str):
        results = {}
        # Escape special characters and create regex pattern
        pattern = re.compile(rf'\b{re.escape(search_str)}\b')  # Exact word match
        for filename, content in code_data.items():
            # Normalize line endings and split
            lines = content.replace('\r\n', '\n').split('\n')
            matches = []
            for line in lines:
                if pattern.search(line):
                    matches.append(line)
            if matches:
                results[filename] = matches
        return results

    search_results = search_codebase(data, query)
    return search_results
