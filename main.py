from fastapi import FastAPI
import routes
from pydantic import BaseModel
app=FastAPI()

app.include_router(routes.router)
@app.get("/")
def index():
    return {"botrra rra"}

@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {'data':"sdf"}

