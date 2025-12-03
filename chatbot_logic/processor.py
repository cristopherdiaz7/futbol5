from typing import Dict, Optional


def parse_text_command(text: str) -> Dict:
    """Parsea un comando en texto y devuelve un dict con la acción comparable
    al protocolo JSON del servidor.

    Ejemplos de entrada:
      - 'ver' -> {'action': 'list'}
      - 'reservar 2025-12-04 18:00 MiEquipo 10' -> {'action': 'reserve', 'slot': '2025-12-04 18:00', 'team': 'MiEquipo', 'players': 10}
      - 'cancelar <id>' -> {'action': 'cancel', 'id': '<id>'}
    """
        try:
            parts = shlex.split(text)
        except Exception:
            parts = text.strip().split()
    if not parts:
        return {"action": "noop"}
    cmd = parts[0].lower()
    if cmd in ("ver", "list"):
        return {"action": "list"}
    if cmd in ("ayuda", "help"):
        return {"action": "help"}
    if cmd == "reservar":
        # minimal parsing: reservar <fecha> <hora> <nombre> <jugadores>
        if len(parts) < 5:
            return {"action": "invalid", "error": "Uso: reservar <fecha> <hora> <nombre> <jugadores>"}
        fecha = parts[1]
        hora = parts[2]
        slot = f"{fecha} {hora}"
            team = parts[3]
            # Soporta nombres con espacios usando comillas
        try:
            players = int(parts[4])
        except Exception:
            players = 10
        return {"action": "reserve", "slot": slot, "team": team, "players": players}
    if cmd == "cancelar":
        if len(parts) < 2:
            return {"action": "invalid", "error": "Uso: cancelar <id>"}
        return {"action": "cancel", "id": parts[1]}
    return {"action": "unknown", "text": text}


if __name__ == '__main__':
    examples = [
        'ver',
        'reservar 2025-12-04 18:00 "Mi Equipo" 10',
        'cancelar 123'
    ]
    for e in examples:
        print(e, '->', parse_text_command(e))
