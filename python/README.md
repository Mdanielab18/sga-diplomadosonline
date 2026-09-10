# Implementación en Python - SGA-DO

En esta carpeta se encuentra la versión funcional en Python correspondiente al prototipo del Sistema de Gestión Académica (SGA-DO).

## Archivo principal

- `sga_do.py`: aplicación de consola completa.

## Archivos generados por el programa

Al ejecutar el sistema se crean/actualizan:

- `alumnos.txt`
- `profesores.txt`
- `certificados_pendientes.txt`

## Funcionalidades

1. Registrar alumnos.
2. Registrar profesores.
3. Registrar hasta 3 notas por alumno.
4. Deshacer la última nota mediante una pila (LIFO).
5. Generar la cola de certificados mediante Queue/FIFO.
6. Mostrar reporte general.
7. Salir guardando los cambios.

## Ejecución

Desde la carpeta `python`:

```bash
python sga_do.py
```

No requiere librerías externas.
