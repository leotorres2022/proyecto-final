<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <form class="login-card" @submit.prevent="handleLogin">
      <h2>Iniciar sesión</h2>

      <label for="username">Usuario</label>
      <input id="username" v-model="username" type="text" name="login" required />

      <label for="password">Contraseña</label>
      <input id="password" v-model="password" type="password" name="password" required />

      <button type="submit" class="login-btn">Ingresar</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import useSociosStore from '@/stores/socios';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const authStore = useAuthStore();
const sociosStore = useSociosStore();
const router = useRouter();

async function handleLogin() {
  try {
    await authStore.login(username.value, password.value);

    const socio = await sociosStore.findByTelefono(username.value);
    if (socio) {
      router.push({ name: 'socios_show', params: { id: socio.id } });
      return;
    }

    router.push('/'); // Si no es socio por teléfono, directo al Home
  } catch (error) {
    alert('Credenciales incorrectas o error de servidor');
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}
.login-card {
  width: 320px;
  padding: 1.5rem;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 6px 18px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}
.login-card h2 {
  margin: 0 0 1rem 0;
  text-align: center;
}
.login-card label {
  margin-top: 0.75rem;
}
.login-card input {
  padding: 0.5rem;
  margin-top: 0.25rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.login-btn {
  margin-top: 1rem;
  padding: 0.6rem;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>