# 🧊 IceExpress — Arquitectura de Microservicios

Sistema de delivery de hielo para pingüinos, construido como challenge de arquitectura de microservicios. Implementa comunicación REST entre servicios, autenticación JWT, patrón Saga con compensación, y Circuit Breaker.

## 🏗️ Arquitectura

| Servicio | Puerto | Responsabilidad |
|---|---|---|
| `auth-service` | 8005 | Registro, login, emisión y validación de JWT |
| `productos-service` | 8001 | CRUD de productos (nombre, tipo de hielo, precio) |
| `inventario-service` | 8002 | Control de stock por producto |
| `pedidos-service` | 8003 | Orquestación de pedidos (consulta precio, descuenta stock, cobra) |
| `pagos-service` | 8004 | Procesamiento simulado de pagos |

Cada servicio tiene su **propia base de datos PostgreSQL** — sin tablas compartidas.

## 🚀 Cómo levantar el sistema

### Requisitos
- Docker Desktop instalado y corriendo
- Git

### Levantar todo con un solo comando
```bash
docker compose up --build
```

Esto levanta los 10 contenedores (5 servicios + 5 bases de datos).

### Documentación interactiva de cada servicio

Una vez levantado, cada servicio expone su Swagger UI:

- Auth: http://localhost:8005/docs
- Productos: http://localhost:8001/docs
- Inventario: http://localhost:8002/docs
- Pedidos: http://localhost:8003/docs
- Pagos: http://localhost:8004/docs

## 🔐 Flujo de uso

1. `POST /registro` en auth-service → crear usuario
2. `POST /login` en auth-service → obtener `access_token`
3. Usar ese token en el header `Authorization: Bearer <token>` en todos los demás servicios
4. `POST /productos` → crear un producto
5. `POST /inventario` → cargar stock
6. `POST /pedidos` → crear pedido (orquesta automáticamente precio, stock y pago)

## 🛡️ Patrones implementados

- **JWT**: autenticación entre servicios con clave compartida
- **Saga con compensación**: si el pago falla, el stock se repone automáticamente
- **Circuit Breaker**: si un servicio falla repetidamente, las llamadas se cortan al instante (cerrado → abierto → semi-abierto → cerrado)
- **Retry**: reintentos automáticos ante fallos técnicos transitorios
- **Logging centralizado**: formato unificado en los 5 servicios

## 📁 Estructura del proyecto