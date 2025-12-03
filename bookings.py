import json
import os
import threading
import uuid
from typing import List, Dict, Optional


class BookingManager:
    def __init__(self, path: str = "data/bookings.json"):
        self.path = path
        self.lock = threading.RLock()
        self.bookings: List[Dict] = []
        self._load()

    def _load(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            self.bookings = []
            self._save()
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.bookings = json.load(f)
        except Exception:
            self.bookings = []
            self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.bookings, f, indent=2, ensure_ascii=False)

    def list_bookings(self) -> List[Dict]:
        with self.lock:
            return list(self.bookings)

    def find_by_slot(self, slot: str) -> Optional[Dict]:
        with self.lock:
            for b in self.bookings:
                if b.get("slot") == slot:
                    return b
        return None

    def reserve(self, slot: str, team: str, players: int, user: str = None) -> Dict:
        with self.lock:
            if self.find_by_slot(slot) is not None:
                return {"ok": False, "error": "Turno ya reservado para ese horario"}
            booking = {
                "id": str(uuid.uuid4()),
                "slot": slot,
                "team": team,
                "players": int(players),
            }
            if user:
                booking["user"] = user
            
            self.bookings.append(booking)
            self._save()
            return {"ok": True, "booking": booking}

    def cancel(self, booking_id: str, user: str = None) -> Dict:
        with self.lock:
            for i, b in enumerate(self.bookings):
                if b.get("id") == booking_id:
                    # if reservation has a user and a user is provided, enforce match
                    owner = b.get("user")
                    if owner and user and owner != user:
                        return {"ok": False, "error": "No autorizado: sólo el creador puede cancelar esta reserva"}
                    if owner and not user:
                        return {"ok": False, "error": "No autorizado: se requiere usuario para cancelar esta reserva"}
                    removed = self.bookings.pop(i)
                    self._save()
                    return {"ok": True, "booking": removed}
        return {"ok": False, "error": "ID de reserva no encontrado"}

    def cancel_by_user(self, user: str) -> Dict:
        if not user:
            return {"ok": False, "error": "Se requiere usuario para cancelar reservas personales"}
        removed = []
        with self.lock:
            remaining = []
            for b in self.bookings:
                if b.get('user') == user:
                    removed.append(b)
                else:
                    remaining.append(b)
            if not removed:
                return {"ok": False, "error": "No se encontraron reservas del usuario"}
            self.bookings = remaining
            self._save()
        return {"ok": True, "removed": removed}


if __name__ == "__main__":
    bm = BookingManager()
    print("Reservas actuales:")
    print(json.dumps(bm.list_bookings(), indent=2, ensure_ascii=False))
