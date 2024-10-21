from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path  # Importa Path
import os
import subprocess

router = APIRouter()
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    # Guarda el archivo LaTeX en el directorio de uploads
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Genera el PDF usando pdflatex
    pdf_filename = os.path.join(UPLOAD_DIR, file.filename.replace('.tex', '.pdf '))
    print(f"Archivo LaTeX guardado en: {file_location}")
    print(f"Archivo PDF esperado en: {pdf_filename}")

    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=batchmode', '-output-directory', UPLOAD_DIR, str(file_location)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("PDF generation completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error generating PDF:")
        print(e.stderr.decode())
        raise HTTPException(status_code=500, detail="Error generating PDF")

    # Devuelve el archivo PDF
    return FileResponse(pdf_filename)


@router.get("/pdf")
async def get_pdf():
    PDF_PATH = Path(UPLOAD_DIR) / "helloworld.pdf"  # Asegúrate de que la ruta sea correcta
    if PDF_PATH.exists():
        print(f"Devolviendo el PDF: {PDF_PATH}")  # Mensaje de progreso
        return FileResponse(PDF_PATH)
    else:
        print(f"PDF no encontrado: {PDF_PATH}")  # Mensaje de error
        raise HTTPException(status_code=404, detail="PDF not found")
