"""Script de entrada para ejecutar modo servidor o cliente.

Uso:
  python run_chatbot.py --mode server
  python run_chatbot.py --mode client
"""
import argparse


def main():
    parser = argparse.ArgumentParser(prog='run_chatbot')
    parser.add_argument('--mode', choices=['server', 'client'], default='client')
    args = parser.parse_args()
    if args.mode == 'server':
        # import del paquete servidor
        from socket_srv.server import main as server_main
        server_main()
    else:
        from socket_srv.client import main as client_main
        client_main()


if __name__ == '__main__':
    main()
