from fastapi import APIRouter, status
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/error", status_code=status.HTTP_200_OK)
async def get_error_img():
    return FileResponse("./src/assets/error.png")


@router.get("/stopwatch", status_code=status.HTTP_200_OK)
async def get_stopwatch_img():
    return FileResponse("./src/assets/stopwatch.png")
