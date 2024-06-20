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
        s.sendall(b"sensor_presion")
        try:
            while True:
                # Generar un valor de presión aleatorio entre 5 y 20 kPa
                pressure = random.uniform(5, 20)
                
                # Convertir el valor de presión a cadena y codificarlo
                message = f"{pressure:.2f}"
                
                # Enviar el valor de presión al servidor
                s.sendall(message.encode('utf-8'))
                
                print(f"Enviado: {message} kPa")
                
                # Esperar 0.5 segundos antes de enviar el siguiente valor
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Interrumpido por el usuario. Cerrando conexión...")
        finally:
            s.close()

if __name__ == "__main__":
    main()