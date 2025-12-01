# Security Policy

## Supported Versions

Esta sección indica cuáles versiones del Sistema de Barbería están actualmente soportadas con actualizaciones de seguridad.

| Version | Supported          |
| ------- | ----------------- |
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :x:               |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:               |

> Nota: Las versiones son referenciales y corresponden a iteraciones internas de desarrollo. Mantén siempre actualizado tu entorno de desarrollo y dependencias.

## Reporting a Vulnerability

Si encuentras una vulnerabilidad de seguridad en este proyecto, sigue estos pasos:

1. Envía un correo a **nextechnologyadm@gmail.com** con el asunto: `[Security] Reporte de vulnerabilidad`.
2. Incluye:
   - Descripción detallada del problema.
   - Pasos para reproducirlo.
   - Entorno donde fue detectado (versión, sistema operativo, navegador, etc.).
3. Recibirás confirmación de recepción dentro de 24-48 horas.
4. Nuestro equipo evaluará la vulnerabilidad y te mantendrá informado sobre:
   - Confirmación de que se aceptó o descartó.
   - Plazo estimado para la corrección si se acepta.
5. Por favor, **no publiques** la vulnerabilidad hasta que se haya solucionado y aprobado públicamente.

## Good Practices

- Mantén tus dependencias actualizadas, especialmente Django y paquetes de seguridad.
- No compartas credenciales ni archivos de configuración sensibles en el repositorio.
- Usa siempre entornos virtuales y variables de entorno para información sensible.
