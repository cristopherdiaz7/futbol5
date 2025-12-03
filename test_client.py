import socket
import json

HOST = '127.0.0.1'
PORT = 5000

def send_and_recv(sock, obj):
    s = sock.makefile(mode='rw', encoding='utf-8')
    s.write(json.dumps(obj, ensure_ascii=False) + "\n")
    s.flush()
    resp = s.readline()
    return resp

def main():
    with socket.create_connection((HOST, PORT)) as sock:
        print('Conectado al servidor')
        print('Listando reservas (inicial):')
        print(send_and_recv(sock, {"action":"list"}))

        print('Intentando crear reserva de prueba...')
        resp = send_and_recv(sock, {"action":"reserve", "slot":"2025-12-10 18:00", "team":"EquipoPrueba", "players":10})
        print('Respuesta reserva:', resp)
        try:
            r = json.loads(resp)
            if r.get('ok'):
                bid = r.get('booking', {}).get('id')
                print('ID creada:', bid)
                print('Cancelando reserva...')
                print(send_and_recv(sock, {"action":"cancel", "id": bid}))
        except Exception as e:
            print('No se pudo parsear respuesta:', e)

if __name__ == '__main__':
    main()
