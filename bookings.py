import json
import os
import threading
import uuid
from typing import List, Dict, Optional


class BookingManager:
    def __init__(self, path: str = "data/bookings.json"):
        self.path = path
        self.lock = threading.Lock()
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

    def reserve(self, slot: str, team: str, players: int) -> Dict:
        with self.lock:
            if self.find_by_slot(slot) is not None:
                return {"ok": False, "error": "Turno ya reservado para ese horario"}
            booking = {
                "id": str(uuid.uuid4()),
                "slot": slot,
                "team": team,
                "players": int(players),
            }
            self.bookings.append(booking)
            self._save()
            return {"ok": True, "booking": booking}

    def cancel(self, booking_id: str) -> Dict:
        with self.lock:
            for i, b in enumerate(self.bookings):
                if b.get("id") == booking_id:
                    removed = self.bookings.pop(i)
                    self._save()
                    return {"ok": True, "booking": removed}
        return {"ok": False, "error": "ID de reserva no encontrado"}


if __name__ == "__main__":
    bm = BookingManager()
    print("Reservas actuales:")
    print(json.dumps(bm.list_bookings(), indent=2, ensure_ascii=False))
