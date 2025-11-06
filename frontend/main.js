// Usar rutas relativas permite que el frontend funcione cuando se sirve desde el mismo origen
const backendUrl = ''; // dejar vacío para usar rutas relativas: `${backendUrl}/users/login` -> '/users/login'

const form = document.getElementById('loginForm');
const msgEl = document.getElementById('message');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  msgEl.textContent = '';
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;

  if (!username || !password) {
    msgEl.textContent = 'Ingrese usuario y contraseña.';
    msgEl.style.color = 'red';
    return;
  }

    try {
    const res = await fetch(`${backendUrl}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('access_token', data.access_token);
      msgEl.textContent = 'Login correcto. Token guardado en localStorage.';
      msgEl.style.color = 'green';
    } else {
      msgEl.textContent = data.msg || 'Error al iniciar sesión';
      msgEl.style.color = 'red';
    }
  } catch (err) {
    msgEl.textContent = 'No se pudo conectar con el backend.';
    msgEl.style.color = 'red';
    console.error(err);
  }
});