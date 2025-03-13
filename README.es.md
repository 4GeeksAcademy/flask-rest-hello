<a href="https://www.breatheco.de"><img height="280" align="right" src="https://github.com/4GeeksAcademy/flask-rest-hello/blob/main/docs/assets/badge.png?raw=true"></a>

# Plantilla de Flask para Desarrolladores Junior

Crea API's con Flask en minutos, [📹 mira el tutorial en video](https://youtu.be/ORxQ-K3BzQA).

- [Documentación extensa aquí](https://start.4geeksacademy.com).
- Integrado con Pipenv para la gestión de paquetes.
- Despliegue rápido a render.com o heroku con `$ pipenv run deploy`.
- Uso de archivo `.env`.
- Integración de SQLAlchemy para la abstracción de bases de datos.

## 1) Instalación

Esta plantilla se instala en unos segundos si la abres gratis con Codespaces (recomendado) o Gitpod.
Omite estos pasos de instalación y salta al paso 2 si decides usar cualquiera de esos servicios.

> Importante: La plantilla está hecha para python 3.10 pero puedes cambiar la `python_version` en el Pipfile.

Los siguientes pasos se ejecutan automáticamente dentro de gitpod, si estás haciendo una instalación local debes hacerlos manualmente:

```sh
pipenv install;
psql -U root -c 'CREATE DATABASE example;'
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```

> Nota: Los usuarios de Codespaces pueden conectarse a psql escribiendo: `psql -h localhost -U gitpod example`

## 2) Cómo empezar a codificar

Hay una API de ejemplo funcionando con una base de datos de ejemplo. Todo tu código de aplicación debe escribirse dentro de la carpeta `./src/`.

- src/main.py (aquí es donde debes codificar tus endpoints)
- src/models.py (tus tablas de base de datos y lógica de serialización)
- src/utils.py (algunas clases y funciones reutilizables)
- src/admin.py (agrega tus modelos al administrador y gestiona tus datos fácilmente)

Para una explicación más detallada, busca el tutorial dentro de la carpeta `docs`.

## Recuerda migrar cada vez que cambies tus modelos

Debes migrar y actualizar las migraciones por cada actualización que hagas a tus modelos:

```bash
$ pipenv run migrate # (para hacer las migraciones)
$ pipenv run upgrade  # (para actualizar tu base de datos con las migraciones)
```

## Generar un diagrama de la base de datos

Si deseas visualizar la estructura de tu base de datos en forma de diagrama, puedes generarlo con el siguiente comando:

```bash
$ pipenv run diagram
```

Este comando generará un archivo con el diagrama de la base de datos basado en los modelos definidos en `src/models.py`.

## Verifica tu API en vivo

1. Una vez que ejecutes el comando `pipenv run start` tu API comenzará a ejecutarse en vivo y podrás abrirla haciendo clic en la pestaña "ports" y luego haciendo clic en "open browser".

> ✋ Si estás trabajando en una nube de codificación como [Codespaces](https://docs.github.com/en/codespaces/developing-in-codespaces/forwarding-ports-in-your-codespace#sharing-a-port) o [Gitpod](https://www.gitpod.io/docs/configure/workspaces/ports#configure-port-visibility) asegúrate de que tu puerto reenviado sea público.

## Publica/Despliega tu sitio web!

Esta plantilla está 100% lista para desplegarse con Render.com y Heroku en cuestión de minutos. Por favor lee la [documentación oficial al respecto](https://start.4geeksacademy.com/deploy).

### Contribuidores

Esta plantilla fue construida como parte del [Bootcamp de Codificación](https://4geeksacademy.com/us/coding-bootcamp) de 4Geeks Academy por [Alejandro Sanchez](https://twitter.com/alesanchezr) y muchos otros contribuidores. Descubre más sobre nuestro [Curso de Desarrollador Full Stack](https://4geeksacademy.com/us/coding-bootcamps/part-time-full-stack-developer), y [Bootcamp de Ciencia de Datos](https://4geeksacademy.com/us/coding-bootcamps/datascience-machine-learning).

Puedes encontrar otras plantillas y recursos como este en la [página de github de la escuela](https://github.com/4geeksacademy/).