from fastapi import APIRouter
import os

router = APIRouter()

@router.delete("/finish")
async def finish(repo_name: str):
    #check if repo with that name exists under folder uploads
    repo_path = f"uploads/{repo_name}"
    if not os.path.exists(repo_path):
        return {
            "message": f"Repository '{repo_name}' not found."
        }
    #delete the repo folder and all its contents
    try:
        for root, dirs, files in os.walk(repo_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(repo_path)
        return {
            "message": f"Repository '{repo_name}' and all its contents have been deleted successfully."
        }
    except Exception as e:
        return {
            "message": f"An error occurred while deleting the repository: {str(e)}"
        }
