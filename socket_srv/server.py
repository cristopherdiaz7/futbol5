import socket
import threading
import json
from services.reservation_service import ReservationService


HOST = '0.0.0.0'
PORT = 5000


def handle_client(conn: socket.socket, addr, service: ReservationService):
    print(f"[socket_srv] Conexión desde {addr}")
    f = conn.makefile(mode='rw', encoding='utf-8')
    try:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except Exception:
                resp = {"ok": False, "error": "JSON inválido"}
                f.write(json.dumps(resp, ensure_ascii=False) + "\n")
                f.flush()
                continue

            action = req.get('action')
            if action == 'list':
                resp = {"ok": True, "bookings": service.list_reservations()}
            elif action == 'reserve':
                slot = req.get('slot')
                team = req.get('team')
                players = req.get('players', 10)
                user = req.get('user')
                if not slot or not team:
                    resp = {"ok": False, "error": "Faltan campos: slot o team"}
                else:
                    resp = service.reserve(slot, team, players, user)
            elif action == 'cancel':
                booking_id = req.get('id')
                user = req.get('user')
                if booking_id:
                    resp = service.cancel(booking_id, user)
                else:
                    # cancel all bookings for this user
                    resp = service.cancel_by_user(user)
            elif action == 'help':
                resp = {"ok": True, "help": "Comandos: list, reserve, cancel"}
            else:
                resp = {"ok": False, "error": "Acción desconocida"}

            f.write(json.dumps(resp, ensure_ascii=False) + "\n")
            f.flush()
    except Exception as e:
        print(f"[socket_srv] Error con cliente {addr}: {e}")
    finally:
        try:
            f.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        print(f"[socket_srv] Conexión cerrada {addr}")


def main(host: str = HOST, port: int = PORT):
    service = ReservationService()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"[socket_srv] Servidor escuchando en {host}:{port}")
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr, service), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("[socket_srv] Servidor detenido por teclado")


if __name__ == '__main__':
    main()
