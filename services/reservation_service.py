from bookings import BookingManager
from typing import Dict, List
from datetime import datetime


class ReservationService:
    """Capa de servicio que encapsula el `BookingManager`.

    Este servicio proporciona métodos que pueden ser reutilizados por el servidor
    y por capas superiores (p. ej. web o CLI).
    """

    def __init__(self, path: str = "data/bookings.json"):
        self._manager = BookingManager(path)

    def list_reservations(self) -> List[Dict]:
        return self._manager.list_bookings()

    def reserve(self, slot: str, team: str, players: int, user: str = None) -> Dict:
        # Validate slot time is on the allowed hours
        # expected slot format: 'YYYY-MM-DD HH:MM'
        try:
            date_part, time_part = slot.strip().split(None, 1)
        except Exception:
            return {"ok": False, "error": "Formato de slot inválido. Use 'YYYY-MM-DD HH:MM'"}

        allowed_hours = [f"{h:02d}:00" for h in range(14, 24)]
        # Accept only exact hour slots (minutes must be 00)
        if time_part not in allowed_hours:
            return {"ok": False, "error": f"Horario no permitido. Horarios válidos: {', '.join(allowed_hours)}"}

        # Validate slot is not in the past
        try:
            slot_dt = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
        except Exception:
            return {"ok": False, "error": "Formato de slot inválido. Use 'YYYY-MM-DD HH:MM'"}

        now = datetime.now()
        if slot_dt < now:
            return {"ok": False, "error": "No se pueden reservar turnos en el pasado"}

        # Delegate to BookingManager which already checks duplicates
        return self._manager.reserve(slot, team, players, user)

    def cancel(self, booking_id: str, user: str = None) -> Dict:
        # Only allow cancellation by the creator (user) if booking has a user
        return self._manager.cancel(booking_id, user)

    def cancel_by_user(self, user: str) -> Dict:
        return self._manager.cancel_by_user(user)


if __name__ == '__main__':
    s = ReservationService()
    print('Reservas actuales:', s.list_reservations())
