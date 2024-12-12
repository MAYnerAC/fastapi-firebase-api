#
# uvicorn main:app --reload
#
# C:/Users/OVALTECH/Desktop/fastapi-firebase-api/config/sistema-turismo-24169-firebase-adminsdk-fhe9j-2ea146511f.json
#
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Inicializar Firebase Admin SDK
cred = credentials.Certificate('C:/Users/OVALTECH/Desktop/fastapi-firebase-api/config/sistema-turismo-24169-firebase-adminsdk-fhe9j-2ea146511f.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Crear una instancia de FastAPI
app = FastAPI()

# Definir el modelo Pydantic para validar los datos
class Usuario(BaseModel):
    nombre: str
    edad: int

# Rutas CRUD

# 1. Crear un usuario
@app.post("/usuarios/", response_model=Usuario)
async def crear_usuario(usuario: Usuario):
    doc_ref = db.collection('usuarios').add(usuario.dict())
    # Acceder correctamente al ID
    return {**usuario.dict(), 'id': doc_ref[1].id}  # doc_ref[1] es el documento insertado


# 2. Obtener todos los usuarios
@app.get("/usuarios/", response_model=List[Usuario])
async def obtener_usuarios():
    usuarios_ref = db.collection('usuarios')
    docs = usuarios_ref.stream()
    usuarios = [Usuario(**doc.to_dict()) for doc in docs]
    return usuarios

# 3. Obtener un usuario por ID
@app.get("/usuarios/{usuario_id}", response_model=Usuario)
async def obtener_usuario(usuario_id: str):
    doc = db.collection('usuarios').document(usuario_id).get()
    if doc.exists:
        return Usuario(**doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# 4. Actualizar un usuario
@app.put("/usuarios/{usuario_id}", response_model=Usuario)
async def actualizar_usuario(usuario_id: str, usuario: Usuario):
    doc_ref = db.collection('usuarios').document(usuario_id)
    doc_ref.update(usuario.dict())
    return {**usuario.dict(), 'id': usuario_id}

# 5. Eliminar un usuario
@app.delete("/usuarios/{usuario_id}")
async def eliminar_usuario(usuario_id: str):
    doc_ref = db.collection('usuarios').document(usuario_id)
    doc_ref.delete()
    return {"message": "Usuario eliminado"}