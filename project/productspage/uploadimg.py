from project.productspage import productpic
from fastapi import FastAPI, UploadFile, File, APIRouter

router = APIRouter(
    prefix="/uploadfile",
    tags=['uploadfile']
)


@router.post('/')
async def create_file(files: UploadFile = File(...)):
    file_name = "some"

    file_location = f"{file_name}"

    with open(file_location, "wb+") as file_object:
        productpic.put(files.filename, files.file)
        return {"info": f"file '{file_name}' saved at '{file_location}'"}


def uploadimage(file: UploadFile = File(...)):
    with open(f'{file.filename}', "wb") as buffer:
        productpic.copyfileobj(file.file, buffer)
