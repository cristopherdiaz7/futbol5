import json
from pathlib import Path

BOOKINGS = Path(__file__).resolve().parents[1] / 'data' / 'bookings.json'


def assign_user(username: str = 'cristo'):
    if not BOOKINGS.exists():
        print('No existe data/bookings.json')
        return
    with open(BOOKINGS, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception:
            print('Error leyendo bookings.json')
            return

    changed = 0
    for b in data:
        if not b.get('user'):
            b['user'] = username
            changed += 1

    if changed > 0:
        with open(BOOKINGS, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'Asignado usuario "{username}" a {changed} reserva(s).')
    else:
        print('No se encontraron reservas sin propietario.')


if __name__ == '__main__':
    import sys
    user = sys.argv[1] if len(sys.argv) > 1 else 'cristo'
    assign_user(user)
