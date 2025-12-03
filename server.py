import socket
import threading
import json
from bookings import BookingManager


HOST = '0.0.0.0'
PORT = 5000


def handle_client(conn: socket.socket, addr, manager: BookingManager):
    print(f"Conexión desde {addr}")
    # use makefile for convenient line-based IO
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
                resp = {"ok": True, "bookings": manager.list_bookings()}
            elif action == 'reserve':
                slot = req.get('slot')
                team = req.get('team')
                players = req.get('players', 10)
                if not slot or not team:
                    resp = {"ok": False, "error": "Faltan campos: slot o team"}
                else:
                    resp = manager.reserve(slot, team, players)
            elif action == 'cancel':
                booking_id = req.get('id')
                if not booking_id:
                    resp = {"ok": False, "error": "Falta id"}
                else:
                    resp = manager.cancel(booking_id)
            elif action == 'help':
                resp = {"ok": True, "help": "Comandos: list, reserve, cancel"}
            else:
                resp = {"ok": False, "error": "Acción desconocida"}

            f.write(json.dumps(resp, ensure_ascii=False) + "\n")
            f.flush()
    except Exception as e:
        print(f"Error con cliente {addr}: {e}")
    finally:
        try:
            f.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        print(f"Conexion cerrada {addr}")


def main():
    manager = BookingManager()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr, manager), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("Servidor detenido por teclado")


if __name__ == '__main__':
    main()
