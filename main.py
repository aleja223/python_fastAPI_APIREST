# API REST: Interfas de programación de Aplicaciones para compartir recursos

from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable nonde tendrá todas las caracteristicas de una API REST
app = FastAPI()


# Acá definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre:str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int


# simularemos una based de datos
cursos_db = []


# CRUD: Read (lectura) GET ALL: Leeremos todos los cursos que haya en la db


@app.get("/cursos/", response_model=list[Curso])
def obtener_cursos():
    return cursos_db


# CRUD: Create (escribir) POST: agregamos un nuevo recurso a nuestra base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4())  # Usamos UUID para generar un ID único e irrepetible
    cursos_db.append(curso)
    return curso


# CRUD: Read (lecura) GET (individual): Leeremos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos le primera coincidencia del array devuelve 
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# CRUD: Update (Actualizar/Modificar) PUT: Modificamos un recurso que coincida con el id que le mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos le primera coincidencia del array devuelve 
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el índice exacto donde está el curso en nuestra lista (db)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD: Delete (borrado/baja) DELETE: Eliminaremos un recurso que coincida con el ID que mandamos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos le primera coincidencia del array devuelve 
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso