import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 5000


def send_request(sock_file, req: dict) -> dict:
    sock_file.write(json.dumps(req, ensure_ascii=False) + "\n")
    sock_file.flush()
    resp_line = sock_file.readline()
    if not resp_line:
        return {"ok": False, "error": "No response from server"}
    try:
        return json.loads(resp_line)
    except Exception:
        return {"ok": False, "error": "Respuesta inválida"}


def print_help():
    print("Comandos disponibles:")
    print("  ayuda                     - muestra esta ayuda")
    print("  ver                       - ver reservas actuales")
    print("  reservar                  - iniciar reserva paso a paso (recomendado)")
    print("     o: reservar <fecha> <hora> <nombre>  - atajo rápido (jugadores = 10)")
    print("     ejemplo interactivo:")
    print("       reservar    -> luego te pide fecha, hora, nombre del equipo y jugadores")
    print("     ejemplo atajo:")
    print("       reservar 2025-12-04 18:00 \"Mi Equipo\"")
    print("  cancelar                  - cancelar una de tus reservas (te mostrará las tuyas para elegir)")
    print("  salir                     - cerrar cliente")


def repl(sock_file):
    username = input('Ingrese su nombre de usuario: ').strip()
    if not username:
        username = 'anonimo'
    print(f"Hola, {username}. Escribe 'ayuda' para ver comandos.")
    while True:
        try:
            cmd = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nCerrando cliente')
            break
        if not cmd:
            continue
        parts = cmd.split()
        if parts[0].lower() in ('salir', 'exit', 'quit'):
            break
        if parts[0].lower() in ('ayuda', 'help'):
            print_help()
            continue
        if parts[0].lower() == 'ver':
            req = {"action": "list", "user": username}
            resp = send_request(sock_file, req)
            if resp.get('ok'):
                items = resp.get('bookings', [])
                if not items:
                    print('No hay reservas registradas')
                else:
                    print('Reservas:')
                    for b in items:
                        user = b.get('user') if b.get('user') else '(sin usuario)'
                        print(f"- Reserva: {b.get('slot')} | equipo: {b.get('team')} | jugador/es: {b.get('players')} | user: {user}")
            else:
                print('Error:', resp.get('error'))
            continue
        if parts[0].lower() == 'reservar':
            # If user provided a full command use it, otherwise ask step-by-step
            if len(parts) >= 4:
                # quick form: reservar YYYY-MM-DD HH:MM Name
                fecha = parts[1]
                hora = parts[2]
                slot = f"{fecha} {hora}"
                # team might be quoted in shell; join middle parts if needed
                team = parts[3]
                players = 10
            else:
                # interactive prompts with available-hours view
                print('Reserva interactiva: vas a ingresar los datos del turno.')
                fecha = input('Fecha (YYYY-MM-DD): ').strip()

                # Ask server for existing bookings to show occupied hours for that date
                try:
                    resp_list = send_request(sock_file, {"action": "list"})
                    existing = resp_list.get('bookings', []) if resp_list.get('ok') else []
                except Exception:
                    existing = []

                # allowed hours 14:00..23:00
                allowed_hours = [f"{h:02d}:00" for h in range(14, 24)]
                occupied = set()
                for b in existing:
                    s = b.get('slot', '')
                    if s.startswith(fecha):
                        parts = s.split()
                        if len(parts) >= 2:
                            occupied.add(parts[1])

                print('Horarios para', fecha)
                for h in allowed_hours:
                    mark = '(ocupado)' if h in occupied else '(disponible)'
                    print(f"  {h} {mark}")

                # ask for hour and validate
                while True:
                    hora = input('Elige una hora de las listadas (HH:MM): ').strip()
                    if hora not in allowed_hours:
                        print('Hora inválida — debe ser una hora completa entre 14:00 y 23:00.')
                        continue
                    if hora in occupied:
                        print('Ese horario ya está ocupado, elige otro.')
                        continue
                    break

                team = input('Nombre del equipo (puede tener espacios): ').strip()
                # players fixed to 10 (futbol 5)
                players = 10
                slot = f"{fecha} {hora}"

            try:
                req = {"action": "reserve", "slot": slot, "team": team, "players": int(players), "user": username}
            except Exception:
                print('Error: datos inválidos para la reserva')
                continue

            resp = send_request(sock_file, req)
            if resp.get('ok'):
                b = resp.get('booking')
                user_show = b.get('user') if b.get('user') else username
                print(f"Reserva confirmada: {b.get('slot')} | equipo: {b.get('team')} | user: {user_show}")
            else:
                print('Error:', resp.get('error'))
            continue
        if parts[0].lower() == 'cancelar':
            # interactive cancel: request user's bookings and ask which to cancel
            resp_list = send_request(sock_file, {"action": "list", "user": username})
            if not resp_list.get('ok'):
                print('Error:', resp_list.get('error'))
                continue
            items = resp_list.get('bookings', [])
            user_bookings = [b for b in items if b.get('user') == username]
            if not user_bookings:
                print('No tienes reservas para cancelar.')
                continue
            print('Tus reservas:')
            for idx, b in enumerate(user_bookings, start=1):
                print(f"  {idx}) {b.get('slot')} | {b.get('team')}")
            choice = input('Elige el número de la reserva a cancelar (o Enter para cancelar): ').strip()
            if not choice:
                print('Cancelación abortada')
                continue
            try:
                ci = int(choice)
            except Exception:
                print('Opción inválida')
                continue
            if not (1 <= ci <= len(user_bookings)):
                print('Opción fuera de rango')
                continue
            to_cancel = user_bookings[ci - 1]
            booking_id = to_cancel.get('id')
            req = {"action": "cancel", "id": booking_id, "user": username}
            resp = send_request(sock_file, req)
            if not resp.get('ok'):
                print('Error:', resp.get('error'))
            else:
                b = resp.get('booking')
                print(f"Reserva cancelada: {b.get('slot')} | equipo: {b.get('team')}")
            continue
        print('Comando no reconocido. Usa "ayuda" para ver comandos.')


def main():
    try:
        sock = socket.create_connection((HOST, PORT))
    except Exception as e:
        print('No se pudo conectar al servidor:', e)
        sys.exit(1)
    f = sock.makefile(mode='rw', encoding='utf-8')
    try:
        repl(f)
    finally:
        try:
            f.close()
        except Exception:
            pass
        try:
            sock.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
