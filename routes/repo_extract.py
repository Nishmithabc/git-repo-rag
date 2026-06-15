from fastapi import APIRouter,UploadFile,HTTPException,File
from utils.repo_parsing import repo_process

router=APIRouter()
@router.post('/upload-zipfile')
async def upload_repository(zip_file: UploadFile = File(...)):
    try:
        result = await repo_process(zip_file)
        return {
            "message": "Repository processed successfully.",
            "repository": result["repo_name"],
            "files_indexed": len(result["files"]),
            "files": result["files"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))