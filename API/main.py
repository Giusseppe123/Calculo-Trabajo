from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware  # Importa CORSMiddleware

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permite solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

class Jugador(BaseModel):
    nombre: str
    apellido: str
    numero_camiseta: int
    equipo: Optional[str] = None
    posicion: str
    edad: int 

lista_jugadores: List[Jugador] = [
    Jugador(
        nombre="Andres",
        apellido="Arvelo",
        numero_camiseta=10,
        equipo="Barcelona",
        posicion="Delantero",
        edad=30
    )
]

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de jugadores"}

@app.post("/jugadores")
def crear_jugador(jugador: Jugador):
    for jugador_existente in lista_jugadores:
        if jugador_existente.numero_camiseta == jugador.numero_camiseta:
            raise HTTPException(status_code=400, detail="El jugador ya existe")
    lista_jugadores.append(jugador)
    return {"mensaje": f"jugador {jugador.nombre} creado"}

@app.get("/jugadores/listado")
def mostrar_jugadores():
    return lista_jugadores

@app.put("/jugadores/{numero_camiseta}")
def modificar_jugador(numero_camiseta: int, jugador: Jugador):
    for jugador_existente in lista_jugadores:
        if jugador_existente.numero_camiseta == numero_camiseta:
            jugador_existente.nombre = jugador.nombre
            jugador_existente.apellido = jugador.apellido
            jugador_existente.equipo = jugador.equipo
            jugador_existente.posicion = jugador.posicion
            jugador_existente.edad = jugador.edad
            return {"mensaje": f"jugador {jugador.nombre} modificado"}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")
            
@app.delete("/jugadores/{numero_camiseta}")
def eliminar_jugador(numero_camiseta: int):
    for jugador_existente in lista_jugadores:
        if jugador_existente.numero_camiseta == numero_camiseta:
            lista_jugadores.remove(jugador_existente)
            return {"mensaje": f"jugador {jugador_existente.nombre} eliminado"}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")