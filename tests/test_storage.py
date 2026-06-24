import io
import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers
from app.services.storage_service import StorageService


@pytest.mark.asyncio
async def test_fluxo_completo_armazenamento_minio():
    storage_service = StorageService()

    conteudo_original = b"Conteudo de teste para validacao do MinIO com aioboto3."
    nome_ficheiro = "documento_teste_integracao.txt"
    content_type_original = "text/plain"

    ficheiro_fastapi = UploadFile(
        file=io.BytesIO(conteudo_original),
        filename=nome_ficheiro,
        headers=Headers({"content-type": content_type_original}),
    )

    try:
        url_retornada = await storage_service.upload_file(
            ficheiro_fastapi, nome_ficheiro
        )

        assert url_retornada is not None
        assert nome_ficheiro in url_retornada

        dados_baixados, content_type_baixado = await storage_service.download_file(
            nome_ficheiro
        )

        assert dados_baixados == conteudo_original
        assert content_type_baixado == content_type_original

    finally:
        await storage_service.delete_file(nome_ficheiro)

        with pytest.raises(Exception):
            await storage_service.download_file(nome_ficheiro)
