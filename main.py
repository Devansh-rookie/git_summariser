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

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# async def get_combined_data_internal(owner: str, repo: str, branch: str):
#     """Shared data fetcher used by multiple endpoints"""
#     os.makedirs("results", exist_ok=True)
#     contents = fetch_repo_contents(owner, repo, branch)
#     with open("results/files_data.json", 'w') as f:
#         json.dump(contents, f)
#     return {
#         "owner": owner,from flask_cors import CORS
#         "repo": repo,
#         "branch": branch,
#         "data": [
#             {"type": "repo_contents", "data": contents},
#             {"type": "repo_details", "data": fetch_repo_details(owner, repo)},
#             {"type": "repo_structure", "data": fetch_repo_structure(owner, repo, branch)},
#             {"type": "file_types", "data": fetch_file_types()}
#         ]
#     }
#
async def get_combined_data_internal(owner: str, repo: str, branch: str):
    try:
        contents = fetch_repo_contents(owner, repo, branch)

        # Handle GitHub API errors first
        if isinstance(contents, dict) and 'message' in contents:
            raise HTTPException(502, detail=f"GitHub API Error: {contents['message']}")

        # Create directory if missing
        os.makedirs("results", exist_ok=True)

        with open("results/files_data.json", 'w') as f:
            json.dump(contents, f)

        return {
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
        raw_data = await get_combined_data_internal(owner, repo, branch)

        data = raw_data['data'][0]['data']
        print(raw_data)
        print(data)
                # "owner_info": raw_data['data'][1]['data']['owner'],
        file_type_count = (raw_data['data'][3]['data'])
        if(file_type_count is not None):
            file_type_count = len(file_type_count)

        return {
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

    except Exception as e:
        raise HTTPException(500, detail=f"Summary generation failed: {str(e)}")
