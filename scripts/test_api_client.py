import socket
import json
from datetime import datetime, timedelta

HOST = '127.0.0.1'
PORT = 5000


def send(req):
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        f = s.makefile(mode='rw', encoding='utf-8')
        f.write(json.dumps(req, ensure_ascii=False) + "\n")
        f.flush()
        resp = f.readline()
        try:
            return json.loads(resp)
        except Exception:
            return {'ok': False, 'error': 'invalid json', 'raw': resp}


if __name__ == '__main__':
    print('== LIST BEFORE ==')
    print(send({'action': 'list'}))

    # reserve a slot tomorrow at 15:00 (allowed hour)
    slot_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    slot = f"{slot_date} 15:00"
    req = {'action': 'reserve', 'slot': slot, 'team': 'EquipoCI', 'players': 10, 'user': 'integration_test'}
    print('\n== RESERVE ==')
    print('Request:', req)
    print(send(req))

    print('\n== LIST AFTER ==')
    print(send({'action': 'list'}))
