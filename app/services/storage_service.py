import aioboto3
from fastapi import UploadFile
import logging
from botocore.exceptions import ClientError
from botocore.config import Config

from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Serviço assíncrono para armazenamento de arquivos."""

    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket_name = settings.MINIO_BUCKET_NAME

        self.bucket_config = {
            "service_name": "s3",
            "endpoint_url": settings.MINIO_ENDPOINT,
            "aws_access_key_id": settings.MINIO_ACCESS_KEY,
            "aws_secret_access_key": settings.MINIO_SECRET_KEY,
            "region_name": "us-east-1",
            "config": Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        }

    async def _ensure_bucket_exists(self, s3_client):
        try:
            await s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")

            if error_code in ("404", "NoSuchBucket"):
                await s3_client.create_bucket(Bucket=self.bucket_name)
            else:
                raise

    async def upload_file(self, file: UploadFile, filename: str) -> str:
        async with self.session.client(**self.bucket_config) as s3_client:
            await self._ensure_bucket_exists(s3_client)

            await s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                filename,
                ExtraArgs={"ContentType": file.content_type},
            )

        logger.info(f"Arquivo {filename} enviado com sucesso!")

        return f"{settings.MINIO_ENDPOINT}/{self.bucket_name}/{filename}"

    async def download_file(self, filename: str) -> tuple[bytes, str]:
        async with self.session.client(**self.bucket_config) as s3:
            response = await s3.get_object(Bucket=self.bucket_name, Key=filename)

            content_type: str = response.get("ContentType", "application/octet-stream")
            file_data: bytes = await response["Body"].read()

            return file_data, content_type

    async def delete_file(self, filename: str) -> None:
        async with self.session.client(**self.bucket_config) as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=filename)
            logger.info(
                f"Ficheiro {filename} removido com sucesso do bucket {self.bucket_name}."
            )
