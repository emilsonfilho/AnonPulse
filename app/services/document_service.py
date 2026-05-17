import os 
import shutil

from fastapi import UploadFile

from app.schemas.document_schema import DocumentResponse

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DocumentService:
    def __init__(self, repository):
        self.repository = repository

    async def upload(self, assignment_id: int, file: UploadFile) -> DocumentResponse:
        extension = file.filename.split(".")[-1] if "." in file.filename else ""

        await file.seek(0, 2)
        size_bytes = file.file.tell()
        await file.seek(0)

        document_data = {
            "original_filename": file.filename,
            "content_type": file.content_type,
            "extension": extension,
            "size_bytes": size_bytes
        }

        new_document = await self.repository.create(document_data)

        file_path = f"{UPLOAD_DIR}/{new_document.id}.{new_document.extension}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return DocumentResponse.model_validate(new_document)