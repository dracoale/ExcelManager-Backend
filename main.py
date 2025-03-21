from fastapi import FastAPI
from routes import router
from pydantic import BaseModel
app=FastAPI()

app.include_router(router)
@app.get("/")
def index():
    return {"botrra rra"}

@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {'data':"sdf"}

