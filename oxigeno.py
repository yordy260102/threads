import socket
import random
import time

# Configuración del cliente
SERVER_IP = '127.0.0.1'  # Dirección IP del servidor (usa 'localhost' si el servidor está en la misma máquina)
SERVER_PORT = 5000      # Puerto de conexión del servidor

def main():
    # Crear un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectar al servidor
        s.connect((SERVER_IP, SERVER_PORT))
        print(f"Conectado al servidor {SERVER_IP} en el puerto {SERVER_PORT}")
        # Identificar al cliente como sensor oxigeno
        s.sendall(b"sensor_oxigeno")
        try:
            while True:
                # Generar un valor de oxígeno disuelto aleatorio entre 0% y 100%
                oxygen_level = random.uniform(0, 100)
                
                # Convertir el valor de oxígeno disuelto a cadena y codificarlo
                message = f"{oxygen_level:.2f}"
                
                # Enviar el valor de oxígeno disuelto al servidor
                s.sendall(message.encode('utf-8'))
                
                print(f"Enviado: {message}% de oxígeno disuelto")
                
                # Esperar 0.3 segundos antes de enviar el siguiente valor
                time.sleep(0.3)
        except KeyboardInterrupt:
            print("Interrumpido por el usuario. Cerrando conexión...")
        finally:
            s.close()

if __name__ == "__main__":
    main()