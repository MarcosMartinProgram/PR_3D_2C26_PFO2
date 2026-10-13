# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

API REST modular desarrollada en **Python**, **Flask** y **SQLite** para la gestión y autenticación de usuarios con persistencia relacional, hashing criptográfico de credenciales y control de sesiones mediante cookies HTTP firmadas.

El proyecto se compone de tres partes principales:
- **Backend API (`servidor.py`)**: Servicio RESTful con persistencia en SQLite, consultas parametrizadas y seguridad mediante Werkzeug.
- **Cliente CLI (`cliente.py`)**: Interfaz de consola interactiva con persistencia de cookies mediante `requests.Session`.
- **Panel Web (`index.html`)**: Cliente web liviano para pruebas interactivas directas con soporte de CORS y envío de credenciales.

---

## 🛠️ Tecnologías y Requisitos

- **Python 3.10+**
- **Flask** (>= 3.0.0)
- **Flask-CORS** (>= 4.0.0)
- **python-dotenv** (>= 1.0.0)
- **Requests** (>= 2.31.0)
- **SQLite3** (motor relacional integrado)

---

## 📁 Estructura del Proyecto

```text
PFO2/
├── servidor.py          # API REST Flask, endpoints y gestión de base de datos
├── cliente.py           # Cliente interactivo de consola (CLI)
├── index.html           # Panel de pruebas web interactivo
├── requirements.txt     # Lista de dependencias del entorno
├── .env.example         # Plantilla de variables de configuración
├── gestion_tareas.db    # Base de datos SQLite (generada al iniciar)
└── README.md            # Documentación del proyecto
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio y entrar al directorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd PFO2
```

### 2. Crear y activar el entorno virtual
- **En Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **En Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (Opcional)
Crea un archivo `.env` en la raíz del proyecto para personalizar la configuración:
```env
FLASK_PORT=5000
FLASK_DEBUG=True
SECRET_KEY=clave_secreta_segura_de_desarrollo
DB_NAME=gestion_tareas.db
```

### 5. Iniciar el servidor
```bash
python servidor.py
```
> La base de datos y las tablas necesarias se inicializan automáticamente en el primer arranque. El servicio quedará disponible en `http://127.0.0.1:5000`.

---

## 📡 Endpoints de la API REST

| Método | Endpoint | Descripción | Autenticación Requerida |
|---|---|---|:---:|
| `POST` | `/registro` | Registra un usuario con contraseña hasheada | No |
| `POST` | `/login` | Valida credenciales e inicia la sesión | No |
| `GET` | `/tareas` | Vista protegida del panel de tareas | **Sí** |
| `POST` | `/logout` | Destruye la sesión activa | **Sí** |

---

### 📑 Especificación de Rutas

#### 1. Registro de Usuario
- **Ruta:** `POST /registro`
- **Headers:** `Content-Type: application/json`
- **Cuerpo (JSON):**
  ```json
  {
    "usuario": "marcos",
    "contraseña": "miPasswordSeguro123"
  }
  ```
- **Respuestas:**
  - `201 Created`:
    ```json
    { "mensaje": "Usuario 'marcos' registrado con éxito" }
    ```
  - `400 Bad Request`: Faltan datos requeridos en el cuerpo.
  - `409 Conflict`: El nombre de usuario ya se encuentra registrado.

---

#### 2. Inicio de Sesión
- **Ruta:** `POST /login`
- **Headers:** `Content-Type: application/json`
- **Cuerpo (JSON):**
  ```json
  {
    "usuario": "marcos",
    "contraseña": "miPasswordSeguro123"
  }
  ```
- **Respuestas:**
  - `200 OK` *(emite cookie de sesión `session`)*:
    ```json
    {
      "mensaje": "Bienvenido/a marcos. Inicio de sesión exitoso.",
      "usuario": "marcos"
    }
    ```
  - `401 Unauthorized`: Usuario inexistente o contraseña incorrecta.

---

#### 3. Panel de Tareas (Protegido)
- **Ruta:** `GET /tareas`
- **Respuestas:**
  - `200 OK`: Devuelve la vista HTML personalizada para el usuario autenticado.
  - `401 Unauthorized`:
    ```json
    { "error": "Acceso denegado. Debe iniciar sesión primero." }
    ```

---

#### 4. Cierre de Sesión
- **Ruta:** `POST /logout`
- **Respuestas:**
  - `200 OK`:
    ```json
    { "mensaje": "Sesión cerrada correctamente" }
    ```

---

## 🧪 Pruebas del Sistema

### Opción 1: Cliente CLI (`cliente.py`)
Manteniendo el servidor en ejecución, abre una segunda terminal y corre:
```bash
python cliente.py
```
El cliente cuenta con un menú interactivo numérico que conserva la sesión entre peticiones mediante `requests.Session()`:
1. Registrar nuevo usuario.
2. Iniciar sesión.
3. Consultar ruta protegida `/tareas`.
4. Cerrar sesión.
5. Salir.

### Opción 2: Panel Web (`index.html`)
Abre `index.html` en tu navegador para realizar pruebas directas sobre la interfaz gráfica con soporte para CORS y envío automático de cookies de sesión (`withCredentials`).

---

## 🔒 Consideraciones de Seguridad

1. **Almacenamiento Criptográfico de Contraseñas:**  
   Se utiliza `werkzeug.security.generate_password_hash` con salting automático para evitar el almacenamiento de texto plano y mitigar ataques por tablas arcoíris.
2. **Protección contra Inyección SQL:**  
   Todas las consultas hacia SQLite utilizan sentencias parametrizadas (`?`) en lugar de concatenación de cadenas.
3. **Sesiones HTTP Seguras:**  
   La autenticación descansa en cookies de sesión firmadas con `SECRET_KEY`, impidiendo su manipulación en el lado del cliente.