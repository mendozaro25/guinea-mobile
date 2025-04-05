```markdown
# Guinea Mobile API

![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-latest-green) ![Uvicorn](https://img.shields.io/badge/Uvicorn-latest-brightgreen)

Este es un proyecto backend desarrollado con **FastAPI**, un framework moderno y rápido para construir APIs en Python. El servidor está implementado con **Uvicorn**, un servidor ASGI de alto rendimiento.

---

## Descripción del Proyecto

Este proyecto proporciona una API RESTful para gestionar [inserta aquí la funcionalidad principal, como usuarios, productos, etc.]. Está diseñado para ser escalable, eficiente y fácil de integrar con otros sistemas.

---

## Características Principales

- **FastAPI**: Framework moderno y rápido para construir APIs.
- **Uvicorn**: Servidor ASGI de alto rendimiento.
- **Validación de Datos**: Integración con Pydantic para validación automática de datos.
- **Documentación Automática**: Documentación interactiva generada automáticamente con Swagger UI y ReDoc.
- **Escalabilidad**: Diseñado para manejar múltiples solicitudes concurrentes.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python**: Versión 3.8 o superior.
- **Pip**: Administrador de paquetes de Python.
- **Virtualenv** (opcional): Para crear entornos virtuales.

---

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/mendozaro25/guinea-mobile.git
   cd guinea-mobile
   ```

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución del Proyecto

Para ejecutar el servidor de desarrollo, utiliza el siguiente comando:

```bash
uvicorn main:app --reload
```

- `main`: Es el nombre del archivo principal (sin la extensión `.py`).
- `app`: Es la instancia de FastAPI creada en el archivo principal.
- `--reload`: Habilita el modo de recarga automática durante el desarrollo.

Una vez iniciado el servidor, puedes acceder a la documentación interactiva en las siguientes URLs:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## Pruebas

Para ejecutar las pruebas unitarias, utiliza el siguiente comando:

```bash
pytest
```

Asegúrate de que todas las pruebas pasen antes de realizar cambios importantes en el código.

---

## Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
```

