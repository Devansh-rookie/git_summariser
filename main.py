from fastapi import FastAPI, HTTPException
import json
import os
import logging
from get_file_dat_API import fetch_repo_contents, fetch_repo_details, fetch_repo_structure
from try_summarize import get_dependencies, summarize_the_entire_thing, create_the_summaries
from variable_matching import findAllUsingGrep, findAllOccurrencesVariable
from get_file_types import fetch_file_types
import traceback

app = FastAPI()

# async def get_combined_data_internal(owner: str, repo: str, branch: str):
#     """Shared data fetcher used by multiple endpoints"""
#     os.makedirs("results", exist_ok=True)
#     contents = fetch_repo_contents(owner, repo, branch)
#     with open("results/files_data.json", 'w') as f:
#         json.dump(contents, f)
#     return {
#         "owner": owner,
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
                {"type": "repo_contents", "data": contents},
                {"type": "repo_details", "data": fetch_repo_details(owner, repo)},
                {"type": "repo_structure", "data": fetch_repo_structure(owner, repo, branch)},
                {"type": "file_types", "data": fetch_file_types()}
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Data processing failed: {traceback.format_exc()}")
        raise HTTPException(500, detail=str(e))



"""Get combined repository data with dynamic parameters
Example request:
/api/fetch?owner=Devansh-rookie&repo=git_summariser&branch=main
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
                "total_files": len(raw_data['data'][0]['data']),
                "file_types_count": file_type_count,
                "entire_file_summary": summarize_the_entire_thing(data),
                "all_summaries": create_the_summaries(data),
                "dependencies": get_dependencies(data)
            },
            "metadata": {
                "repo": repo,
                "branch": branch,
            }
        }

    except Exception as e:
        raise HTTPException(500, detail=f"Summary generation failed: {str(e)}")
