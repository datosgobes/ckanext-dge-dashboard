# ckanext-dge-dashboard

`ckanext-dge-dashboard` es una extensión para CKAN utilizada en la plataforma datos.gob.es para generar y gestionar información de *dashboard* a partir de datos de CKAN.

> [!TIP]
> Guía base y contexto del proyecto: https://github.com/datosgobes/datos.gob.es

## Descripción

- Añade un plugin CKAN para funcionalidades relacionadas con *dashboard*.
- Incluye comandos *paster* para inicialización y generación de salidas (CSV/JSON).

## Requisitos

### Compatibilidad
Compatibilidad con versiones de CKAN:

| CKAN version | Compatible?                                                                 |
|--------------|-----------------------------------------------------------------------------|
| 2.8          | ❌ No (>= Python 3)                                                          |
| 2.9          | ✅ Yes  |
| 2.10         | ❓ Unknown |
| 2.11         | ❓ Unknown |

### Dependencias

- Una instancia de CKAN.

## Instalación

```sh
pip install -e .
```

## Configuración

Activa el plugin en tu configuración de CKAN:

```ini
ckan.plugins = … dge_dashboard
```

### Plugins

- `dge_dashboard`

## Tests

```sh
pytest --ckan-ini=test.ini ckanext/dge_dashboard/tests
```

## Licencia

Este proyecto se distribuye bajo licencia **GNU Affero General Public License (AGPL) v3.0 o posterior**. Consulta el fichero [`LICENSE`](LICENSE).
