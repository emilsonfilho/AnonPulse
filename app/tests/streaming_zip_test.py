from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.services.exportacao_service import gerar_zip_streaming

app = FastAPI()

@app.get("/exportar-feedbacks")
def exportar_feedbacks():
    zip_stream = gerar_zip_streaming()
    return StreamingResponse(
        gerar_zip_streaming(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=feedbacks.zip"}
    )