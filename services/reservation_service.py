from bookings import BookingManager
from typing import Dict, List


class ReservationService:
    """Capa de servicio que encapsula el `BookingManager`.

    Este servicio proporciona métodos que pueden ser reutilizados por el servidor
    y por capas superiores (p. ej. web o CLI).
    """

    def __init__(self, path: str = "data/bookings.json"):
        self._manager = BookingManager(path)

    def list_reservations(self) -> List[Dict]:
        return self._manager.list_bookings()

    def reserve(self, slot: str, team: str, players: int) -> Dict:
        return self._manager.reserve(slot, team, players)

    def cancel(self, booking_id: str) -> Dict:
        return self._manager.cancel(booking_id)


if __name__ == '__main__':
    s = ReservationService()
    print('Reservas actuales:', s.list_reservations())
