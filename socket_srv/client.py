import os
import socket
import json
from datetime import datetime

# ================= COLORES ================
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', '5000'))


def send_request(action: str, payload: dict = None):
    """Envía una petición al servidor en el formato correcto."""
    payload = payload or {}
    message = {"action": action}
    message.update(payload)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall((json.dumps(message) + "\n").encode("utf-8"))

        data = sock.recv(4096).decode("utf-8")
        return json.loads(data)


# ========= Impresión más bonita ==========
def pretty_print(res):
    print("\n" + CYAN + "======= RESPUESTA DEL SERVIDOR =======" + RESET)

    if res.get("ok"):
        print(GREEN + "✔ Operación exitosa" + RESET)

        # mostrar reserva cuando existe
        if "booking" in res:
            b = res["booking"]
            print(f"{GREEN}¡Turno reservado correctamente!{RESET}\n")
            print(f"{YELLOW}ID:{RESET} {b['id']}")
            print(f"{YELLOW}Fecha/Hora:{RESET} {b['slot']}")
            print(f"{YELLOW}Equipo:{RESET} {b['team']}")
            print(f"{YELLOW}Jugadores:{RESET} {b['players']}")
            print(f"{YELLOW}Usuario:{RESET} {b['user']}")
        # mostrar lista
        elif "bookings" in res:
            print(f"{CYAN}Reservas encontradas:{RESET}")
            if len(res["bookings"]) == 0:
                print(YELLOW + "No hay reservas registradas." + RESET)
            else:
                for b in res["bookings"]:
                    print(f" - {b['slot']} | {b['team']} | {b['players']} jugadores | ID {b['id']}")

        else:
            print(GREEN + "✔ Acción completada." + RESET)

    else:
        print(RED + "❌ Error: " + RESET + str(res.get("error", "Error desconocido")))

    print(CYAN + "======================================\n" + RESET)


# =============== Menú =====================
def menu():
    print("\n" + BLUE + "===== CLIENTE FUTBOL 5 =====" + RESET)
    print("1. Ver reservas")
    print("2. Reservar")
    print("3. Cancelar reserva por ID")
    print("4. Cancelar todas por usuario")
    print("0. Salir")
    return input("Elija una opción: ").strip()


# =============== MAIN =====================
def main():
    while True:
        op = menu()

        if op == "1":
            res = send_request("list")
            pretty_print(res)

        elif op == "2":
            slot = input("Fecha y hora (YYYY-MM-DD HH:MM): ").strip()
            team = input("Nombre del equipo: ").strip()
            players = int(input("Cantidad de jugadores: ").strip())
            user = input("Tu nombre de usuario: ").strip()

            res = send_request("reserve", {
                "slot": slot,
                "team": team,
                "players": players,
                "user": user
            })
            pretty_print(res)

        elif op == "3":
            booking_id = input("ID de la reserva a cancelar: ").strip()
            user = input("Tu usuario: ").strip()

            res = send_request("cancel", {
                "id": booking_id,
                "user": user
            })
            pretty_print(res)

        elif op == "4":
            user = input("Usuario: ").strip()
            res = send_request("cancel", {"user": user})
            pretty_print(res)

        elif op == "0":
            print(YELLOW + "Saliendo del cliente..." + RESET)
            break

        else:
            print(RED + "Opción inválida." + RESET)


if __name__ == "__main__":
    main()
