import socket
import json
import time

HOST = '127.0.0.1'
PORT = 5000

def send_and_recv(s, req):
    s.sendall((json.dumps(req, ensure_ascii=False) + "\n").encode('utf-8'))
    data = b''
    while not data.endswith(b"\n"):
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    try:
        return json.loads(data.decode('utf-8').strip())
    except Exception as e:
        return {'ok': False, 'error': 'invalid response', 'raw': data.decode('utf-8', errors='ignore')}

def main():
    s = socket.create_connection((HOST, PORT))
    try:
        print('Listado inicial:')
        print(send_and_recv(s, {'action': 'list'}))

        print('Creando reserva de prueba...')
        slot = '2025-12-31 20:00'
        resp = send_and_recv(s, {'action': 'reserve', 'slot': slot, 'team': 'EquipoTest', 'players': 10})
        print('Respuesta reserve:', resp)
        if resp.get('ok'):
            bid = resp.get('booking', {}).get('id')
            print('Listado tras reservar:')
            print(send_and_recv(s, {'action': 'list'}))

            print('Cancelando reserva...')
            print(send_and_recv(s, {'action': 'cancel', 'id': bid}))
            print('Listado final:')
            print(send_and_recv(s, {'action': 'list'}))
        else:
            print('No se pudo crear la reserva de prueba')
    finally:
        s.close()

if __name__ == '__main__':
    main()
