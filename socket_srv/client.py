import socket
import json
import sys
from datetime import datetime
from chatbot_logic.processor import parse_text_command

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
    print("  reservar <fecha> <hora> \"nombre equipo\" <jugadores> - reservar turno")
    print("     ejemplo: reservar 2025-12-04 18:00 \"Mi Equipo\" 10")
    print("  cancelar <id>             - cancelar reserva por id")
    print("  salir                     - cerrar cliente")


def validate_slot(slot: str) -> bool:
    try:
        # espera formato 'YYYY-MM-DD HH:MM'
        datetime.strptime(slot, '%Y-%m-%d %H:%M')
        return True
    except Exception:
        return False


def repl(sock_file):
    print("Cliente chatbot conectado. Escribe 'ayuda' para ver comandos.")
    while True:
        try:
            text = input('> ').strip()
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
            req = {"action": "list"}
            resp = send_request(sock_file, req)
            if resp.get('ok'):
                items = resp.get('bookings', [])
                if not items:
                    print('No hay reservas registradas')
                else:
                    print('Reservas:')
                    for b in items:
                        print(f"- id: {b.get('id')} | slot: {b.get('slot')} | equipo: {b.get('team')} | jugadores: {b.get('players')}")
            else:
                print('Error:', resp.get('error'))
            continue
        if action == 'reserve':
            slot = parsed.get('slot')
            team = parsed.get('team')
            players = parsed.get('players', 10)
            if not validate_slot(slot):
                print('Formato de slot inválido. Usar YYYY-MM-DD HH:MM')
                continue
            req = {"action": "reserve", "slot": slot, "team": team, "players": players}
            resp = send_request(sock_file, req)
            if resp.get('ok'):
                b = resp.get('booking')
                print('Reserva creada:', b.get('id'))
            else:
                print('Error:', resp.get('error'))
            continue
        if action == 'cancel':
            booking_id = parsed.get('id')
            if not booking_id:
                print('Usar: cancelar <id>')
                continue
            req = {"action": "cancel", "id": booking_id}
            resp = send_request(sock_file, req)
            if resp.get('ok'):
                print('Reserva cancelada:', resp.get('booking', {}).get('id'))
            else:
                print('Error:', resp.get('error'))
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
