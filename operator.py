import socket
import threading

# Configuración del cliente
SERVER_IP = '127.0.0.1'  # Dirección IP del servidor
SERVER_PORT = 5000      # Puerto de conexión del servidor

def receive_data_from_server(conn):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(data)
    except Exception as e:
        print(f"Error recibiendo datos: {e}")
    finally:
        conn.close()
        print("Conexión con el servidor cerrada.")

def main():
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conectar al servidor
            s.connect((SERVER_IP, SERVER_PORT))
            print(f"Conectado al servidor {SERVER_IP} en el puerto {SERVER_PORT}")

            # Identificar al cliente como operario
            s.sendall(b"operario")
            
            # Esperar a que el operario presione ENTER para comenzar la transmisión
            input("Presione ENTER para comenzar la transmisión")
            s.sendall(b"start")
            
            # Iniciar un hilo para recibir datos del servidor
            receive_thread = threading.Thread(target=receive_data_from_server, args=(s,))
            receive_thread.start()

            # Mantener el programa corriendo hasta que el operario decida finalizar
            while receive_thread.is_alive():
                try:
                    receive_thread.join(0.1)
                except KeyboardInterrupt:
                    print("\nInterrumpido por el usuario. Cerrando conexión...")
                    s.sendall(b"stop")
                    break

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Asegúrese de que el servidor está en funcionamiento.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()