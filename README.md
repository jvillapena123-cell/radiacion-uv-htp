# Tablero Radiación UV · Huachipato Terminal Portuario

Tablero editable para publicar diariamente el índice UV (D.S. 594 Art. 109 b) con descarga de informe PDF.

## Actualización automática del índice UV
- GitHub Actions (`.github/workflows/actualizar-uv.yml`) ejecuta `scripts/actualizar_uv.py` cada 30 min entre 06:00 y 21:00 y publica `datos/uv.json`.
- Fuentes: pronóstico Open-Meteo (modelo CAMS) para Bahía San Vicente + medición de la Red UV de la DMC (estación más cercana) si están los secretos `DMC_USUARIO` y `DMC_TOKEN`.
- El índice del día publicado es el **mayor** entre pronóstico y medición DMC.
- El tablero lee esos datos al abrir y cada 15 min; si no hay datos recientes consulta el pronóstico directamente.
- Corrección manual: ✎ Editar → escribir el índice (queda "INGRESO MANUAL" hasta fin del día) → **↺ Volver a modo automático**.

### Activar la medición DMC
1. Crear cuenta en https://climatologia.meteochile.gob.cl (Iniciar sesión → registrarse) y obtener el token personal (consultas: portalserviciosclimaticos@meteochile.gob.cl).
2. GitHub → Settings → Secrets and variables → Actions → New repository secret: `DMC_USUARIO` (correo) y `DMC_TOKEN`.

## Uso diario
1. Abrir el tablero: el índice UV ya está actualizado.
2. Opcional: mensaje del día, fotos (📷 Fotos) y boletines.
4. **☁ Publicar** (si Firebase está configurado) para que todos vean el mismo informe.
5. **⬇ Descargar PDF** genera `Informe_UV_HTP_AAAA-MM-DD.pdf` en A4.

Modo pantalla (TV sala VIT / portería): agregar `?pantalla=1` a la URL. Oculta la barra y se actualiza cada 10 min.

Sin Firebase, los cambios se guardan en el navegador del equipo que edita; use **⤓ JSON / ⤒ JSON** como respaldo.

## Boletines de seguridad (panel izquierdo)
- El personal toca un boletín y se abre en ventana emergente: ver, **Descargar** o **Cerrar**.
- **Publicados para todos (sin Firebase):** archivos en la carpeta `boletines/` + una entrada en `boletines/boletines.json`.
- **+ Cargar boletín** abre una ventana con clave. Con Firebase se publica para todos (archivos en Firestore, sin plan de pago, hasta 15 MB). Sin Firebase queda guardado solo en ese equipo.
- Formatos: PDF (todas las páginas, también en iPad), imágenes (JPG/PNG) o enlace web.

## Agenda de la semana (panel derecho)
- Muestra las **capacitaciones** (tema, fecha, hora, lugar, relator, quiénes deben asistir) y las **reuniones de seguridad y Comité Paritario** (lugar, día, hora) de la semana en curso (lunes a domingo).
- **📅 Ver todas del mes** abre el mes completo, con navegación ◀ ▶ entre meses.
- Al tocar una actividad se ve el detalle y se puede **agregar al calendario** (Outlook / celular, archivo .ics).
- **+ Agregar** (con clave). Con Firebase lo ve todo el personal; sin Firebase queda en ese equipo. Agenda publicada para todos sin Firebase: `datos/agenda.json`.

## Clave de acceso
- Una sola clave protege **✎ Editar** y **+ Cargar boletín**. El botón **🔒 Bloquear** cierra el acceso.
- Sin Firebase: la clave se valida con el hash en `firebase-config.js` (`HTP_ACCESO.claveSHA256`). Es una protección básica.
- Con Firebase: la clave es la contraseña del usuario `editor@htpchile.cl` en Authentication (protección real del servidor).

## Publicar en GitHub Pages
```bash
git init && git add . && git commit -m "Tablero UV HTP"
git branch -M main
git remote add origin https://github.com/jvillapena123-cell/radiacion-uv-htp.git
git push -u origin main
```
GitHub → Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)`.
URL: `https://jvillapena123-cell.github.io/radiacion-uv-htp/`

## Publicar en Firebase Hosting + nube
1. Crear proyecto en https://console.firebase.google.com
2. Agregar app Web y copiar la configuración en `firebase-config.js`.
3. Activar **Firestore Database** y **Authentication → Correo/contraseña**; crear el usuario `editor@htpchile.cl` con la clave de edición.
4. En Authentication → Configuración → Dominios autorizados, agregar `jvillapena123-cell.github.io` si también se usa GitHub Pages.
5. Reemplazar `TU_PROYECTO` en `.firebaserc` y desplegar:
```bash
npm install -g firebase-tools
firebase login
firebase deploy
```
URL: `https://TU_PROYECTO.web.app`

## Datos en Firestore
- `uv/actual` → informe vigente (con fotos comprimidas, límite ~1 MB).
- `uv_historial/AAAA-MM-DD` → registro diario sin fotos (trazabilidad para fiscalización).

## Archivos
- `index.html` — tablero completo
- `firebase-config.js` — credenciales web de Firebase
- `firestore.rules` — lectura pública, escritura solo usuarios autenticados
- `boletines/` — boletines publicados y su listado `boletines.json`
- `assets/` — logo HTP y fotos base
