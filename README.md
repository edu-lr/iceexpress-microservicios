# 🧊 IceExpress — Sistema de delivery de hielo con microservicios

Este proyecto lo hice para aprender arquitectura de microservicios desde cero. La idea es simple: una app de delivery de hielo para pingüinos (sí, en serio), dividida en 5 servicios independientes que se comunican entre sí por HTTP.

Si estás mirando esto y no entendés algo, o soy yo del futuro olvidándome de cómo funciona, o sos alguien más. En cualquier caso, acá va la explicación.

---

## ¿Qué hay adentro?

Cinco microservicios, cada uno con su propia base de datos PostgreSQL y su propio contenedor Docker:

| Servicio | Puerto | Qué hace |
|---|---|---|
| `auth-service` | 8005 | Login, registro, y genera los tokens JWT |
| `productos-service` | 8001 | CRUD de productos (tipos de hielo, precios) |
| `inventario-service` | 8002 | Controla cuánto stock hay de cada producto |
| `pedidos-service` | 8003 | El que orquesta todo — hace pedidos, consulta precios, descuenta stock, cobra |
| `pagos-service` | 8004 | Simula pagos (85% de chance de que salgan bien, 15% de que fallen) |

Cada servicio tiene su propia base de datos. Nada de tablas compartidas. Si necesitan hablar entre ellos, lo hacen por API.

---

## Cómo levantarlo

Necesitás tener Docker Desktop instalado y corriendo. Nada más.

```bash
git clone <url-del-repo>
cd "Challenge 9"
docker compose up --build
```

Eso levanta los 10 contenedores (5 servicios + 5 bases de datos) y los conecta entre sí. La primera vez tarda un poco porque descarga las imágenes base.

Cuando termina, cada servicio tiene su documentación interactiva (Swagger):
- http://localhost:8005/docs — Auth
- http://localhost:8001/docs — Productos
- http://localhost:8002/docs — Inventario
- http://localhost:8003/docs — Pedidos
- http://localhost:8004/docs — Pagos

---

## Cómo usarlo (el flujo básico)

Todo empieza en auth-service. Sin token, ningún otro endpoint responde.

**1. Registrarse**
```
POST localhost:8005/registro
{"email": "yo@mail.com", "password": "mipassword"}
```

**2. Hacer login y copiar el token**
```
POST localhost:8005/login
{"email": "yo@mail.com", "password": "mipassword"}
```
Te devuelve un `access_token`. Ese token va en el header de todos los requests siguientes:
```
Authorization: Bearer <el token que copiaste>
```
En Swagger, el botón "Authorize" (el candado) te permite pegarlo una sola vez y lo usa en todos los endpoints.

**3. Crear un producto**
```
POST localhost:8001/productos
{"nombre": "Hielo en escamas", "tipo_hielo": "escamas", "precio": 1500}
```

**4. Cargar stock**
```
POST localhost:8002/inventario
{"producto_id": 1, "cantidad": 100}
```

**5. Crear un pedido**
```
POST localhost:8003/pedidos
{"items": [{"producto_id": 1, "cantidad": 5}]}
```
Esto es lo interesante: pedidos-service se encarga solo de consultar el precio real a productos-service, descontar el stock en inventario-service, y cobrar en pagos-service. Vos solo mandás el producto y la cantidad.

---

## Lo que implementé (y por qué)

**JWT entre servicios**
Todos los servicios validan el mismo token con una clave secreta compartida. No necesitan llamarse entre sí para validar — cada uno puede verificar la firma localmente.

**Saga con compensación**
Si el pago falla después de haber descontado stock, el sistema repone el stock automáticamente. Así el inventario nunca queda descontado por un pedido que no se cobró.

**Circuit Breaker**
Si inventario-service (o cualquier otro) falla 3 veces seguidas, pedidos-service deja de llamarlo por 30 segundos en vez de seguir esperando timeouts. Después de ese tiempo prueba de nuevo con una sola llamada. Si funciona, vuelve a la normalidad.

**Retry automático**
Antes de contar un fallo para el circuit breaker, reintenta 2 veces. Solo los errores de red o 500 cuentan — si el servicio responde "no hay stock" (400), eso no es un fallo técnico.

---

## Estructura de carpetas

```
Challenge 9/
├── docker-compose.yml         ← levanta todo junto
├── .env                       ← SECRET_KEY y config compartida (no se sube a git)
│
├── auth-service/
│   ├── app/
│   │   ├── main.py            ← endpoints: /registro y /login
│   │   ├── models.py          ← tabla usuarios
│   │   ├── schemas.py         ← validación de datos con Pydantic
│   │   ├── crud.py            ← lógica de crear y autenticar usuarios
│   │   ├── security.py        ← hash de contraseñas (bcrypt) y JWT
│   │   ├── database.py        ← conexión a PostgreSQL
│   │   └── logger.py          ← configuración de logs
│   ├── Dockerfile
│   └── requirements.txt
│
├── productos-service/         ← misma estructura interna
├── inventario-service/        ← misma estructura interna
├── pagos-service/             ← misma estructura interna
│
└── pedidos-service/
    ├── app/
    │   ├── clients.py         ← llama a los otros 3 servicios por HTTP
    │   ├── circuit_breaker.py ← implementación manual del patrón Circuit Breaker
    │   └── ...                ← misma estructura que los demás
    └── ...
```

---

## Cosas que tener en cuenta

- El archivo `.env` en la raíz tiene la `SECRET_KEY` para JWT. Nunca subir esto a Git (ya está en `.gitignore`).
- `pagos-service` simula pagos: 85% aprobados, 15% rechazados. Si un pedido te da 402, probá de nuevo.
- El circuit breaker vive en `pedidos-service/app/circuit_breaker.py`. Para probarlo: `docker compose stop inventario-service`, intentá crear un pedido 3 veces, después `docker compose start inventario-service` y esperá 30 segundos.
- Los volúmenes de Docker persisten los datos entre reinicios. Si querés arrancar desde cero: `docker compose down -v`.

---

## Stack

- Python 3.12 + FastAPI + Uvicorn
- SQLAlchemy (ORM) + PostgreSQL
- Docker + Docker Compose
- JWT con python-jose + bcrypt con passlib
- httpx para llamadas HTTP entre servicios