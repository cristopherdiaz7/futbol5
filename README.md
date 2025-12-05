# Chatbot Cliente-Servidor - Reserva Cancha Fútbol 5

Proyecto para la cátedra de Computación: chatbot cliente-servidor para reservar una cancha de fútbol 5.

**Descripción**
- Aplicación cliente-servidor basada en TCP con mensajes JSON.
- Servidor multihilo que gestiona reservas (reservar, cancelar, ver).
- Cliente tipo chatbot por terminal en español.
- Persistencia sencilla en `data/bookings.json`.

**Archivos principales**
- `server.py` : servidor TCP multihilo.
- `client.py` : cliente chatbot CLI (terminal).
- `bookings.py`: lógica de reservas y persistencia.
- `data/bookings.json`: archivo de datos (no subir al repo si es necesario).
- `run_server.ps1`, `run_client.ps1`: scripts PowerShell para ejecutar.

**Cómo ejecutar (PowerShell)**

1) Iniciar el servidor (en la carpeta del proyecto):
```powershell
python server.py
```
O:
```powershell
./run_server.ps1
```

2) Iniciar un cliente (en otra terminal):
```powershell
python client.py
```
O:
```powershell
./run_client.ps1
```

**Comandos cliente (ejemplos)**
===== CLIENTE FUTBOL 5 =====
1. Ver reservas
2. Reservar
3. Cancelar reserva por ID
4. Cancelar todas por usuario
0. Salir


***

## Dockerización (opcional, recomendado)

Se incluye un `Dockerfile` y `docker-compose.yml` para ejecutar el servidor de forma reproducible.

Pasos resumidos:

- Copiar `.env.example` a `.env` y ajustar valores si hace falta:

```
HOST=0.0.0.0
PORT=5000
```

- Construir y levantar con `docker compose`:

```powershell
docker compose build
docker compose up
```

- El servicio expondrá el puerto definido en `.env` y la carpeta `data/` se montará como volumen para persistir `bookings.json`.

Con `HOST=0.0.0.0` dentro del contenedor y el puerto mapeado, podés ejecutar el cliente desde tu host con:

```powershell
python run_chatbot.py --mode client
```

Notas:
- El código lee las variables `HOST` y `PORT` desde el entorno (`os.environ`), por lo que no hace falta modificar código para cambiar el puerto.
- Si preferís cargar `.env` automáticamente en desarrollo, podés instalar `python-dotenv` y añadir `from dotenv import load_dotenv; load_dotenv()` en `run_chatbot.py`.
 
Ejecutar el cliente dentro de un contenedor (opcional)
-----------------------------------------------

Si querés ejecutar el cliente desde un contenedor dentro de la red de `docker compose` (útil para pruebas), podés usar:

```powershell
# Ejecuta el cliente de forma interactiva dentro de un contenedor
docker compose run --rm client
```

O usar el helper PowerShell incluido:

```powershell
./run_docker.ps1 -Build
```

Esto levantará el servidor (y podés abrir otra terminal y ejecutar `docker compose run --rm client` para abrir un cliente interactivo conectado a la red de compose).
