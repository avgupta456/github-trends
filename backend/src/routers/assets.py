from fastapi import APIRouter, status
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/error", status_code=status.HTTP_200_OK)
async def main():
    return FileResponse("./src/assets/error.png")
