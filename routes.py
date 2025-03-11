from fastapi import APIRouter,File, UploadFile,Form
import pandas as pd
import os
import csv
import io
import json
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from typing import Dict, List

router = APIRouter()

@router.get("/jkj")
def main():
    return "hoola"

@router.post("/uploadcsv")
async def aupload_file(file: UploadFile = File(...)):
    with open(os.getcwd()+"/"+file.filename,"wb")as myfile:
        content = await file.read()
        content_str = content.decode("utf-8", errors="ignore")  # Convertir de bytes a string
        file_like = io.StringIO(content_str)
        data=  csv.reader(file_like)
        header=next(data)
        
    return header
@router.post("/uploadexcel")
async def aupload_file(file: UploadFile = File(...)):
        # Verificar que el archivo sea .xlsx
    if not file.filename.endswith(".xlsx"):
        return {"error": "Formato de archivo no soportado, solo .xlsx"}

    # Leer el archivo .xlsx en memoria
    contents = await file.read()
    file_stream = io.BytesIO(contents)

    # Cargar el archivo .xlsx con pandas (motor "openpyxl")
    df = pd.read_excel(file_stream, engine="openpyxl")  # Necesita openpyxl instalado

    # Obtener la primera fila como cabecera
    header = df.columns.tolist()
    return header	
@router.post("/convertir")
async def convertir(opcion: int = 1, file: UploadFile = File(...)):
    print(os.getcwd())
    # Guardar el archivo cargado temporalmente
    contents = await file.read()
    temp_file_path = os.path.join("temp", file.filename)

    # Asegúrate de que la carpeta temporal exista
    os.makedirs("temp", exist_ok=True)

    with open(temp_file_path, "wb") as f:
        f.write(contents)

    if opcion == 1:
        # Convertir de CSV a Excel
        df = pd.read_csv(temp_file_path)
        output = io.BytesIO()  # Crear un buffer en memoria
        df.to_excel(output, index=False, engine='openpyxl')  # Convertir a Excel
        output.seek(0)  # Volver al principio del archivo

        # Crear un archivo de Excel temporal para enviar como respuesta
        return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={"Content-Disposition": f"attachment; filename={file.filename.split('.')[0]}.xlsx"})

    else:
        # Convertir de Excel a CSV
        df = pd.read_excel(temp_file_path, sheet_name='Sheet1', engine='openpyxl')
        output = io.BytesIO()  # Crear un buffer en memoria
        df.to_csv(output, index=False)
        output.seek(0)  # Volver al principio del archivo

        # Crear un archivo CSV temporal para enviar como respuesta
        return StreamingResponse(output, media_type='text/csv', headers={"Content-Disposition": f"attachment; filename={file.filename.split('.')[0]}.csv"})
@router.post("/dividir")
async def convertir(columnas_hoja: str = Form(...), file: UploadFile = File(...)):
    # Leer el archivo subido
    columnas_hojas = json.loads(columnas_hoja)
    
       # Leer el contenido del archivo Excel
    contents = await file.read()
    temp_file_path = os.path.join("temp", file.filename)

    # Asegurarse de que el directorio temporal exista
    os.makedirs("temp", exist_ok=True)

    # Guardar el archivo Excel temporalmente
    with open(temp_file_path, "wb") as f:
        f.write(contents)

    # Leer el archivo Excel
    df = pd.read_excel(temp_file_path)

    # Crear un archivo Excel temporal para la salida
    excel_file_path = os.path.join("temp", f"{file.filename.split('.')[0]}_output.xlsx")

    # Crear un objeto ExcelWriter para manejar múltiples hojas
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        for hoja, columnas in columnas_hojas.items():
            # Filtrar las columnas específicas para cada hoja
            df_hoja = df[columnas]
            # Guardar en la hoja especificada
            df_hoja.to_excel(writer, index=False, sheet_name=hoja)

    # Devolver el archivo Excel como respuesta
    return FileResponse(excel_file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={
        "Content-Disposition": f"attachment; filename={file.filename.split('.')[0]}_output.xlsx"
    })

@router.get("/upload")
def aupload_file():
    return os.getcwd()