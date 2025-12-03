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
- `ayuda` : muestra ayuda.
- `ver` : lista reservas y turnos disponibles.
- `reservar 2025-12-04 18:00 MiEquipo 10` : reservar (fecha hora, nombre equipo, cant jugadores).
- `cancelar <id>` : cancela una reserva por su id.
- `salir` : cierra el cliente.

Si quieres, adapto el cliente para usar interfaz gráfica o para desplegar en red dentro de la facultad.

***
