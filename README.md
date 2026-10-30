# ControlLabITERN

**Sistema de Gestión de Laboratorio – Instituto Técnico ITERN**

Sistema de escritorio desarrollado en Python con una interfaz gráfica moderna y una base de datos MySQL local, diseñado para facilitar la administración y el control de los equipos de cómputo, las áreas físicas y los recursos del laboratorio informático.

El proyecto busca centralizar la información del laboratorio, facilitar la consulta y actualización de registros y mejorar el control de los recursos tecnológicos del instituto.

## Características principales

- **Gestión de equipos:** Registro, consulta, edición y eliminación de computadoras.
- **Control de áreas físicas:** Organización de los equipos en las áreas de Laboratorio y Bodega.
- **Inventario general:** Administración de herramientas, periféricos e insumos.
- **Gestión de usuarios:** Registro, consulta, eliminación y actualización de contraseñas.
- **Búsqueda de registros:** Filtrado de información mediante consultas dinámicas.
- **Generación de reportes PDF:** Exportación de información de los equipos.
- **Inicio de sesión:** Autenticación de usuarios mediante credenciales protegidas.

## Módulos del sistema

| Módulo | Descripción |
|---|---|
| Equipos | Administración de computadoras y sus características técnicas. |
| Áreas | Organización de los equipos en Laboratorio y Bodega. |
| Inventario | Control de herramientas, periféricos y cantidades disponibles. |
| Usuarios | Administración de cuentas y contraseñas. |

## Tecnologías utilizadas

- **Python 3:** Lenguaje de programación principal.
- **CustomTkinter:** Desarrollo de la interfaz gráfica.
- **MySQL 8.0:** Sistema de gestión de bases de datos.
- **MySQL Connector:** Comunicación entre Python y MySQL.
- **Bcrypt:** Protección criptográfica de contraseñas.
- **FPDF:** Generación de documentos PDF.
- **Tkinter / ttk:** Componentes gráficos y tablas de información.

## Seguridad informática

El sistema incorpora mecanismos de seguridad basados en recomendaciones del OWASP Top 10:

- **OWASP A02 – Fallos criptográficos:** Protección de contraseñas mediante hashes Bcrypt y sal aleatoria.
- **OWASP A03 – Inyección SQL:** Utilización de consultas parametrizadas para las operaciones con MySQL.
- **OWASP A05 – Configuración y gestión de errores:** Manejo de excepciones y mensajes genéricos para evitar mostrar información técnica sensible al usuario.

## Base de datos

El proyecto utiliza una base de datos local denominada `controllabitern`, organizada en cuatro tablas principales:

- `areas`: Almacena las áreas físicas del instituto.
- `computadoras`: Registra las características y el estado de los equipos.
- `inventario_general`: Almacena herramientas, periféricos e insumos.
- `usuarios`: Gestiona las cuentas y los hashes de las contraseñas.

## Requisitos previos

Para ejecutar el proyecto se necesita:

- Python 3 instalado.
- MySQL Server 8.0.
- MySQL Workbench (recomendado para administrar la base de datos).
- Sistema operativo compatible con CustomTkinter.

## Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/TU-USUARIO/ControlLabITERN.git
```

**2. Ingresar al directorio**

```bash
cd ControlLabITERN
```

**3. Instalar las dependencias**

```bash
pip install customtkinter mysql-connector-python bcrypt fpdf
```

**4. Crear la base de datos**

Ejecutar en MySQL:

```sql
CREATE DATABASE IF NOT EXISTS controllabitern;
```

**5. Configurar la conexión**

Revisar el archivo `conexion_db.py` y establecer los parámetros correspondientes a la instalación local de MySQL:

- Host: `localhost`
- Usuario: Usuario configurado en MySQL.
- Contraseña: Contraseña del usuario de MySQL.
- Base de datos: `controllabitern`.

**6. Ejecutar el sistema**

```bash
python main.py
```

## Funcionamiento

La aplicación inicia mediante una ventana de autenticación. Después de validar las credenciales, permite acceder al panel principal, desde donde se pueden administrar los equipos, las áreas físicas, el inventario general y los usuarios.

El sistema utiliza una conexión directa con MySQL local, por lo que no necesita depender de servicios web ni de una conexión a Internet para realizar sus operaciones habituales.

## Interfaz gráfica

La aplicación utiliza un diseño oscuro denominado Lab Dark, con una combinación de colores orientada a mantener una interfaz organizada y facilitar la visualización de los registros.

## Equipo de desarrollo

Proyecto desarrollado para el Instituto Técnico ITERN.

**Integrantes:**
- Wilmer
- Xiomara
- Tojil
- Daniel

**Fecha de desarrollo:** Octubre de 2026.

---

**ControlLabITERN** – Sistema de Gestión de Laboratorio Informático.

Desarrollado con Python y MySQL.
