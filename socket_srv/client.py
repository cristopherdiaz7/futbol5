import socket
import json
import sys
from datetime import datetime
from chatbot_logic.processor import parse_text_command

HOST = '127.0.0.1'
PORT = 5000


def send_request(sock_file, req: dict) -> dict:
    try:
        sock_file.write(json.dumps(req, ensure_ascii=False) + "\n")
        sock_file.flush()
    except ConnectionResetError:
        return {"ok": False, "error": "Conexión cerrada por el servidor"}
    except Exception as e:
        return {"ok": False, "error": f"Error enviando petición: {e}"}

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
    print("  reservar <fecha> <hora> \"nombre equipo\" - reservar turno (jugadores = 10)")
    print("     ejemplo: reservar 2025-12-04 18:00 \"Mi Equipo\"")
    print("  cancelar                  - cancelar una de tus reservas (te mostrará las tuyas para elegir)")
    print("  salir                     - cerrar cliente")


def validate_slot(slot: str) -> bool:
    try:
        # espera formato 'YYYY-MM-DD HH:MM'
        datetime.strptime(slot, '%Y-%m-%d %H:%M')
        return True
    except Exception:
        return False


def repl(sock_file):
    # Ask for user name immediately when the client starts
    username = input('Ingrese su nombre de usuario: ').strip()
    if not username:
        username = 'anonimo'
    print(f"Hola, {username}. Escribe 'ayuda' para ver comandos.")
    while True:
        try:
            text = input(f'{username}> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nCerrando cliente')
            break
        if not text:
            continue
        parsed = parse_text_command(text)
        action = parsed.get('action')
        if action in ('salir', 'exit', 'quit'):
            break
        if action == 'help':
            print_help()
            continue
        if action == 'list':
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
                        # Do not display internal id; show reservation, team and user
                        print(f"- Reserva: {b.get('slot')} | equipo: {b.get('team')} | jugador/es: {b.get('players')} | user: {user}")
            else:
                print('Error:', resp.get('error'))
            continue
        if action == 'cancel':
            # interactive cancel: get user's bookings and ask which one to cancel
            resp_list = send_request(sock_file, {"action": "list", "user": username})
            if not resp_list.get('ok'):
                print('Error:', resp_list.get('error'))
                continue
            items = resp_list.get('bookings', [])
            # filter only bookings that belong to this user
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
            req = {"action": "cancel", "id": booking_id, "user": username}
            resp = send_request(sock_file, req)
            if not resp.get('ok'):
                print('Error:', resp.get('error'))
            else:
                if 'booking' in resp:
                    b = resp.get('booking')
                    print(f"Reserva cancelada: {b.get('slot')} | equipo: {b.get('team')}")
                elif 'removed' in resp:
                    removed = resp.get('removed', [])
                    print(f"Se cancelaron {len(removed)} reserva(s) para el usuario {username}:")
                    for b in removed:
                        print(f" - {b.get('slot')} | {b.get('team')}")
                else:
                    print('Cancelación procesada')
            continue
        if action == 'invalid':
            print(parsed.get('error'))
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
