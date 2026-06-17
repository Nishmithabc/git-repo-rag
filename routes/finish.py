from fastapi import APIRouter
import os

router = APIRouter()

@router.delete("/delete-repo/{repo_name}")
async def finish(repo_name: str):
    #check if repo with that name exists under folder uploads
    repo_path = f"uploads/{repo_name}"
    if not os.path.exists(repo_path):
        return {
            "message": f"Repository '{repo_name}' not found."
        }
    #check if vector_store folder exists under the repo folder
    vector_store_path = os.path.join(repo_path, "vector_store")
    if os.path.exists(vector_store_path):
        #delete the vector_store folder and all its contents
        try:
            for root, dirs, files in os.walk(vector_store_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(vector_store_path)
        except Exception as e:
            return {
                "message": f"An error occurred while deleting the vector_store: {str(e)}"
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
