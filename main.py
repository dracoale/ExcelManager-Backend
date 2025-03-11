from fastapi import FastAPI
import routes
from pydantic import BaseModel
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (puedes restringirlo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)
app.include_router(routes.router)
@app.get("/")
def index():
    return {"botrra rra"}

@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {'data':"sdf"}

