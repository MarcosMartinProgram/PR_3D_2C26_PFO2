import sys
import requests

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

def menu():
    while True:
        print("\n" + "=" * 45)
        print("   SISTEMA DE GESTIÓN DE TAREAS (CLIENTE)   ")
        print("=" * 45)
        print("1. Registrar nuevo usuario (POST /registro)")
        print("2. Iniciar sesión (POST /login)")
        print("3. Ver panel de tareas (GET /tareas)")
        print("4. Cerrar sesión (POST /logout)")
        print("5. Salir")
        print("-" * 45)
        
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            usuario = input("Ingrese nombre de usuario: ").strip()
            contrasena = input("Ingrese contraseña: ").strip()
            if not usuario or not contrasena:
                print("Error: Los campos no pueden estar vacíos.")
                continue

            try:
                res = session.post(f"{BASE_URL}/registro", json={"usuario": usuario, "contraseña": contrasena})
                print(f"\n[Status {res.status_code}] Respuesta: {res.json()}")
            except requests.exceptions.ConnectionError:
                print("\nError: No se puede conectar con el servidor. ¿Está ejecutándose servidor.py?")

        elif opcion == "2":
            usuario = input("Ingrese nombre de usuario: ").strip()
            contrasena = input("Ingrese contraseña: ").strip()
            if not usuario or not contrasena:
                print("Error: Los campos no pueden estar vacíos.")
                continue

            try:
                res = session.post(f"{BASE_URL}/login", json={"usuario": usuario, "contraseña": contrasena})
                print(f"\n[Status {res.status_code}] Respuesta: {res.json()}")
            except requests.exceptions.ConnectionError:
                print("\nError: No se puede conectar con el servidor.")

        elif opcion == "3":
            try:
                res = session.get(f"{BASE_URL}/tareas")
                if res.status_code == 200:
                    print("\n[Status 200 OK] ¡Acceso concedido!")
                    print("Contenido HTML recibido (primeros 250 caracteres):")
                    print(res.text[:250] + "...")
                else:
                    print(f"\n[Status {res.status_code}] Acceso denegado: {res.json()}")
            except requests.exceptions.ConnectionError:
                print("\nError: No se puede conectar con el servidor.")

        elif opcion == "4":
            try:
                res = session.post(f"{BASE_URL}/logout")
                print(f"\n[Status {res.status_code}] Respuesta: {res.json()}")
            except requests.exceptions.ConnectionError:
                print("\nError: No se puede conectar con el servidor.")

        elif opcion == "5":
            print("Cerrando cliente de consola.")
            sys.exit(0)
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()