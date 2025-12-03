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
