from fastapi import FastAPI

app = FastAPI(
    title="UniShort QR",
    version="0.1.0",
    description="Servicio institucional de acortamiento de URLs y códigos QR - UNL",
)

@app.get("/health")
def health():
    """Verificación de disponibilidad del servicio."""
    return {"status": "ok"}
    