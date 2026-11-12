// Configuración de Firebase para el Tablero UV HTP.
// 1) En https://console.firebase.google.com → Configuración del proyecto → Tus apps → Web (</>)
// 2) Copie aquí los valores de "firebaseConfig".
// Mientras apiKey comience con "TU_", el tablero funciona en modo local (sin nube).
window.FIREBASE_CONFIG = {
  apiKey: "TU_API_KEY",
  authDomain: "TU_PROYECTO.firebaseapp.com",
  projectId: "TU_PROYECTO",
  storageBucket: "TU_PROYECTO.appspot.com",
  messagingSenderId: "000000000000",
  appId: "TU_APP_ID"
};

// ===== Clave de acceso para ✎ Editar y + Cargar boletín =====
// Sin Firebase: se compara contra este hash (para cambiar la clave, pida el nuevo hash).
// Con Firebase: la clave es la contraseña del usuario "usuarioFirebase" en Authentication.
window.HTP_ACCESO = {
  claveSHA256: "7a5acb1bb55cab9686ef55722d762082e1f66bc0d27c1bf673162b6307d49d60",
  usuarioFirebase: "editor@htpchile.cl"
};
