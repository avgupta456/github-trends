from fastapi import APIRouter, status
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/error", status_code=status.HTTP_200_OK, include_in_schema=False)
async def get_error_img():
    return FileResponse("./src/routers/assets/assets/error.png")


@router.get("/stopwatch", status_code=status.HTTP_200_OK, include_in_schema=False)
async def get_stopwatch_img():
    return FileResponse("./src/routers/assets/assets/stopwatch.png")
