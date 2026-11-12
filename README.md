# Tablero Radiación UV · Huachipato Terminal Portuario

Tablero editable para publicar diariamente el índice UV (D.S. 594 Art. 109 b) con descarga de informe PDF.

## Uso diario
1. Abrir el tablero → **⟳ Referencia automática** carga pronóstico de 7 días y curva horaria (modelo Open-Meteo) para Bahía San Vicente.
2. **✎ Editar** → escribir el **índice UV máximo** publicado por la DMC (meteochile.gob.cl). Al escribirlo, el dato queda como oficial y desaparece la etiqueta "Referencia modelo".
3. Agregar mensaje del día, fotos de muelle / bodegas / canchas y ajustar medidas si corresponde.
4. **☁ Publicar** (si Firebase está configurado) para que todos vean el mismo informe.
5. **⬇ Descargar PDF** genera `Informe_UV_HTP_AAAA-MM-DD.pdf` en A4.

Modo pantalla (TV sala VIT / portería): agregar `?pantalla=1` a la URL. Oculta la barra y se actualiza cada 10 min.

Sin Firebase, los cambios se guardan en el navegador del equipo que edita; use **⤓ JSON / ⤒ JSON** como respaldo.

## Boletines de seguridad (panel izquierdo)
- El personal toca un boletín y se abre en ventana emergente: ver, **Descargar** o **Cerrar**.
- **Publicados para todos (sin Firebase):** archivos en la carpeta `boletines/` + una entrada en `boletines/boletines.json`.
- **+ Cargar boletín** abre una ventana con clave. Con Firebase se publica para todos (archivos en Firestore, sin plan de pago, hasta 15 MB). Sin Firebase queda guardado solo en ese equipo.
- Formatos: PDF (todas las páginas, también en iPad), imágenes (JPG/PNG) o enlace web.

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
