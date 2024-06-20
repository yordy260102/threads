import socket
import threading
from datetime import datetime

# Configuraciones del servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

# Variables para manejar conexiones
pressure_socket = None
oxygen_socket = None
operator_socket = None

# Bandera para iniciar transmisión
transmission_started = threading.Event()

# Constantes para el cálculo de la profundidad
DENSITY = 1023.6  # kg/m^3
GRAVITY = 9.81    # m/s^2

# Lock para sincronizar el envío de datos al operario
send_lock = threading.Lock()

def handle_pressure_sensor(conn):
    global operator_socket
    print("Sensor de presión conectado")

    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Recibido del sensor de presión: {data} kPa")
            pressure_kpa = float(data)
            pressure_pa = pressure_kpa * 1000  # Convertir kPa a Pa
            depth = pressure_pa / (DENSITY * GRAVITY)  # Calcular profundidad en metros
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            if operator_socket and transmission_started.is_set():
                message = f"Profundidad: {depth:.2f} m, Tiempo: {timestamp}"
                send_to_operator(message)
    except Exception as e:
        print(f"Error en el sensor de presión: {e}")
    finally:
        conn.close()
        print("Sensor de presión desconectado")

def handle_oxygen_sensor(conn):
    global operator_socket
    print("Sensor de oxígeno conectado")

    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Recibido del sensor de oxígeno: {data}%")
            oxygen_level = float(data)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            if operator_socket and transmission_started.is_set():
                message = f"Oxígeno disuelto: {oxygen_level:.2f}%, Tiempo: {timestamp}"
                send_to_operator(message)
    except Exception as e:
        print(f"Error en el sensor de oxígeno: {e}")
    finally:
        conn.close()
        print("Sensor de oxígeno desconectado")

def handle_operator(conn):
    global operator_socket
    operator_socket = conn
    print("Operario conectado")

    try:
        while True:
            command = conn.recv(1024).decode('utf-8')
            if command.strip().lower() == "start":
                print("Empezando transmisión")
                transmission_started.set()
            elif command.strip().lower() == "stop":
                print("Parando transmisión")
                transmission_started.clear()
    except Exception as e:
        print(f"Error en el operario: {e}")
    finally:
        conn.close()
        print("Operario desconectado")

def send_to_operator(message):
    with send_lock:
        try:
            if operator_socket:
                operator_socket.sendall(message.encode('utf-8'))
                print(f"Enviado al operario: {message}")
        except Exception as e:
            print(f"Error enviando al operario: {e}")

def accept_connections(server_socket):
    global pressure_socket, oxygen_socket

    while True:
        conn, addr = server_socket.accept()
        client_type = conn.recv(1024).decode('utf-8').strip()
        print(f"Conexión recibida de {addr} como {client_type}")

        if client_type == "sensor_presion":
            if not pressure_socket:
                pressure_socket = conn
                threading.Thread(target=handle_pressure_sensor, args=(conn,)).start()
            else:
                print("Sensor de presión ya conectado. Conexión adicional rechazada.")
                conn.close()
        elif client_type == "sensor_oxigeno":
            if not oxygen_socket:
                oxygen_socket = conn
                threading.Thread(target=handle_oxygen_sensor, args=(conn,)).start()
            else:
                print("Sensor de oxígeno ya conectado. Conexión adicional rechazada.")
                conn.close()
        elif client_type == "operario":
            if not operator_socket:
                threading.Thread(target=handle_operator, args=(conn,)).start()
            else:
                print("Operario ya conectado. Conexión adicional rechazada.")
                conn.close()
        else:
            print(f"Cliente desconocido: {client_type}. Conexión cerrada.")
            conn.close()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen()
        print(f"Servidor escuchando en {SERVER_IP}:{SERVER_PORT}")
        
        accept_connections(server_socket)