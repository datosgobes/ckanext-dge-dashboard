# ckanext-dge-dashboard

`ckanext-dge-dashboard` es una extensión para CKAN utilizada en la plataforma [datos.gob.es](https://datos.gob.es/) para generar y gestionar información de *dashboard* a partir de datos de CKAN.

> [!TIP]
> Guía base y contexto del proyecto: https://github.com/datosgobes/datos.gob.es

## Overview

- Añade un plugin CKAN con funcionalidades relacionadas con *dashboard*.
- Incluye comandos *paster* para inicialización y generación de salidas (CSV/JSON).

## Requirements

- Una instancia de CKAN.

### Compatibilidad

Compatibilidad con versiones de CKAN:

| CKAN version | Compatible?                                                                 |
|--------------|-----------------------------------------------------------------------------|
| 2.8          | ❌ No (>= Python 3)                                                          |
| 2.9          | ✅ Yes  |
| 2.10         | ❓ Unknown |
| 2.11         | ❓ Unknown |

## Installation

```sh
pip install -e .
```

## Configuration

Activa el plugin en tu configuración de CKAN:

```ini
ckan.plugins = … dge_dashboard
```

### Plugins

- `dge_dashboard`

### CLI (`ckan`)

> [!NOTE]
> Desde CKAN 2.9, los comandos *paster* se ejecutan mediante el comando `ckan`.
> Consulta la [documentación oficial](https://docs.ckan.org/en/2.9/maintaining/cli.html) para más detalles.

Este repositorio expone los siguientes comandos:

- `dge_dashboard_initdb`
- `dge_dashboard_load`
- `dge_dashboard_json`
- `dge_dashboard_csv`

Ejemplo de uso (ajusta el fichero `.ini` a tu entorno):

```sh
ckan -c /etc/ckan/default/ckan.ini dge_dashboard_initdb
```

## Running the tests

Este repositorio incluye tests; si tu entorno no dispone de `test.ini`, puedes ejecutar directamente el paquete de tests:

```sh
pytest ckanext/dge_dashboard/tests
```

## License

Este proyecto se distribuye bajo licencia **GNU Affero General Public License (AGPL) v3.0 o posterior**. Consulta el fichero [LICENSE](LICENSE).
