// Configuración de Firebase para el Tablero UV HTP.
// 1) En https://console.firebase.google.com → Configuración del proyecto → Tus apps → Web (</>)
// 2) Copie aquí los valores de "firebaseConfig".
// Mientras apiKey comience con "TU_", el tablero funciona en modo local (sin nube).
window.FIREBASE_CONFIG = {
  apiKey: "AIzaSyBEiVXBkuHhJjOxs0LpaC4JitxL_q3rWgU",
  authDomain: "htp-radiacion-uv.firebaseapp.com",
  projectId: "htp-radiacion-uv",
  storageBucket: "htp-radiacion-uv.firebasestorage.app",
  messagingSenderId: "843290153668",
  appId: "1:843290153668:web:2cc4fbfb45c2b44616af91"
};

// ===== Clave de acceso para ✎ Editar y + Cargar boletín =====
// Sin Firebase: se compara contra este hash (para cambiar la clave, pida el nuevo hash).
// Con Firebase: la clave es la contraseña del usuario "usuarioFirebase" en Authentication.
window.HTP_ACCESO = {
  claveSHA256: "7a5acb1bb55cab9686ef55722d762082e1f66bc0d27c1bf673162b6307d49d60",
  usuarioFirebase: "editor@htpchile.cl"
};
