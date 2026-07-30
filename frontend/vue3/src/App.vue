<template>
  <div class="app-container">
   <header>
    <nav class="navbar">
  <ul>
  <li v-for="link in visibleLinks" :key="link.name">
    <router-link :to="link.to">
      <template v-if="link.imagen">
          <img :src="link.imagen" :alt="link.name" class="navbar-logo" />
        </template>

        <template v-else-if="link.icon">
          <i :class="link.icon" class="navbar-icon" :title="link.name"></i>
        </template>

        <template v-else>
          {{ link.name }}
        </template>
    </router-link>
  </li>

  <li>
  <a @click.prevent="manejarAccionUsuario" class="login-link" :title="authStore.isAuthenticated ? 'Logout' : 'Login'">
    <i :class="['pi', authStore.isAuthenticated ? 'pi-sign-out' : 'pi-user', 'icon-user'] "></i>
  </a>
</li>
</ul>
    </nav>



    <div v-if="$route.path === '/'">
    <h1>¿Todavia no sos socio?</h1>
    <button><router-link :to="{name:'socios_create'}">ASOCIATE </router-link></button>
      </div>
    </header>

    <main class="main-content">
      <!-- Solo muestra las imágenes en Home -->
      <div class="imagenes-container" v-if="$route.path === '/'">
        <img src="@/assets/logo-liga.jpg" alt="Logo Liga" class="img-liga" />
        <img src="@/assets/presi.jpg" alt="Presidente" class="img-presi" />
      </div>
      <RouterView />
    </main>
<footer class="footer">
  <div class="footer-grid">

  <div class="footer-section">
  <h4>Sobre Nosotros</h4>
  <p>El Centro de Entrenamiento Formando Futuro es una institución deportiva dedicada a fomentar el fútbol y los valores del deporte en jóvenes y adultos desde 2018. Con una fuerte presencia en la región, impulsamos el desarrollo atlético, la inclusión y el trabajo en equipo dentro y fuera del campo.</p>
</div>


   <div class="footer-section">
  <h4>Contacto</h4>
  <p><i class="pi pi-envelope" style="margin-right: 8px;"></i> contacto@formandofuturo.edu.ar</p>
  <p><i class="pi pi-whatsapp" style="margin-right: 8px;"></i> 2920 123456</p>
  <p><i class="pi pi-map-marker" style="margin-right: 8px;"></i> Blvd. Ituzaingó 270, Viedma, Río Negro</p>
   </div>


    <div class="footer-section">
      <h4>Accesos Rápidos</h4>
        <ul>
  <li v-for="link in visibleLinks" :key="link.name">
    <router-link :to="link.to">{{ link.name }}</router-link>
  </li>

  <li>
  <a @click.prevent="manejarAccionUsuario" class="login-link" :title="authStore.isAuthenticated ? 'Logout' : 'Login'">
    <i :class="['pi', authStore.isAuthenticated ? 'pi-sign-out' : 'pi-user', 'icon-user'] "></i>
  </a>
</li>
</ul>
    </div>

    <div class="footer-section">
      <h4>Seguinos</h4>
      <ul class="social-links">
        <li><a href="https://facebook.com/formando.futuro.ceff" target="_blank"><i class="pi pi-facebook"></i> Formando Futuro</a></li>
        <li><a href="https://instagram.com/formando.futuro.oficial" target="_blank"><i class="pi pi-instagram"></i> Formando Futuro Oficial</a></li>

      </ul>
    </div>

  </div>

  <div class="footer-bottom">
    <p>© 2025 Formando Futuro CEFF — Todos los derechos reservados.</p>
  </div>
</footer>


  </div>
  </template>

<script setup lang="ts">
import 'primeicons/primeicons.css'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue'
import useCarritoStore  from '@/stores/carrito';
const carritoStore = useCarritoStore()
const router = useRouter()
const authStore = useAuthStore()
const totalLinks = [
  { 
    name: 'HOME', 
    to: '/', 
    groups: ['public'], 
    imagen: new URL('@/assets/galeria/formando_futuro.png', import.meta.url).href,
  },
  { name: 'CLUB', to: { name: 'club' }, groups: ['public'] },
  { name: 'TIENDA', to: { name: 'tienda' }, groups: ['socio'] },
  { name: 'GALERIA', to: { name: 'galeria' }, groups: ['public'] },
  { name: 'SOCIOS', to: { name: 'socios_list' }, groups: ['admin', 'profe', 'socio'] },
  { name: 'COMPRAS', to: { name: 'compras_list' }, groups: ['admin'] },
  { name: 'DIVISIONES', to: { name: 'division_home' }, groups: ['public'] },
  { name: 'CARRITO', to: { name: 'carrito' }, groups: ['socio'], icon: 'pi pi-shopping-cart' },
];

const visibleLinks = computed(() => {
  // Buscamos 'groups' únicamente dentro de 'user'. 
  // Si 'user' no existe o está vacío, le asignamos un arreglo vacío []
  const userGroups: string[] = authStore.user?.groups || [];

  return totalLinks.filter(link => {
    // 1. Si la ruta incluye 'public', la ve cualquiera
    if (link.groups.includes('public')) {
      return true;
    }
    
    // 2. Comparamos los grupos requeridos con los grupos del usuario logueado
    return link.groups.some((group: string) => userGroups.includes(group));
  });
});
const manejarAccionUsuario = () => {
  if (authStore.isAuthenticated) {
    // Si ya está logueado, podés hacer que cierre sesión
    authStore.logout(); // Asegurate de que tu store tenga la función logout
    carritoStore.limpiarCarrito(); // Limpia el carrito al cerrar sesión
    router.push({ name: 'login' });
  } else {
    // Si no está logueado, va directo a la pantalla de login
    router.push({ name: 'login' });
  }
};


</script>

<style scoped>


html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Evita el scroll horizontal */
}
.app-container {
  display: flex;
  flex-direction: column;
  width: 100vw; /* Asegura el ancho completo */
  min-height: 100vh;
}
.navbar {
  background: #169d3e;
  padding: 0 40px;
  width: 100%;
  box-sizing: border-box;
}

.navbar ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  align-items: center;
  justify-content: space-between;
}

.navbar li {
  text-align: center;
  flex: 1;
}

.navbar a {
  display: block;
  font-size: 1.8rem;
  padding: 18px 24px;
  text-decoration: none;
  color: white;
  font-weight: bold;
  transition: background-color 0.3s ease, letter-spacing 0.3s ease;
}

.navbar a:hover {
  background-color: #1aae4d; /* Verde más claro en hover */
  letter-spacing: 0.5px;     /* Separación suave de letras */
  text-decoration: underline;
}
.navbar-logo {
  height: 40px;          
  width: auto;
  object-fit: contain;
  display: block;        
}


.navbar a:has(.navbar-logo):hover {
  background-color: transparent; 
  text-decoration: none;         
  padding: 0px 4px;              
}

.navbar a:has(.navbar-logo):hover .navbar-logo {
  opacity: 0.8;
  transform: scale(1.02);       
  transition: all 0.2s ease;
}

/* Estilos para el main */
.main-content {
  flex: 1;
 

}

.imagenes-container {
  display: flex;
  width: 100%;
  max-width: 1200px;
  height: 640px; /* Más alto */
  gap: 20px;
  margin: 0 auto;
}

.img-presi {
  height: 100%;
  width: 100%;
  border-radius: 12px;
  object-fit: cover;
  background: #fff;
  flex: 2;
}

.img-liga {
  height: 100%;
  width: 100%;
  border-radius: 12px;
  object-fit: contain; /* No deforma el logo */
  background: #fff;
  flex: 1;
}
h1 {
  text-align: center;
  font-family: "Arial Rounded MT Bold", "Arial Rounded", Arial, sans-serif;
}
button {
  display: block;
  margin: 20px auto;
  padding: 12px 32px;
  font-size: 20px;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-family: "Arial Rounded MT Bold", "Arial Rounded", Arial, sans-serif;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}

button:hover {
  background: #447453;
}

/* Estilos para el footer */
.footer {
    background-color: #007BFF;
  color: #fff;
    padding: 60px 20px;
  font-family: 'Segoe UI', sans-serif;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 80px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

.footer-section h4 {
  color: #fff;
  margin-bottom: 15px;
  font-size: 20px;
}

.footer-section p,
.footer-section ul,
.footer-section a {
  font-size: 0.8rem;
  line-height: 1.6;
  color: #fff;
  text-decoration: none;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 10px;
}

.social-links li {
  display: flex;
  align-items: center;
  gap: 8px;
}

.social-links li i {
  font-size: 1.5rem;
}

.footer-bottom {
  text-align: center;
  margin-top: 50px;
  font-size: 14px;
  color: #fff;
}

/* Responsive estilos */

.navbar ul,
.footer ul {
  height: 44px; /* Más bajo */
}

.navbar a,
.footer a {
  font-size: 15px; /* Más chico */
  padding: 8px 0;
}

.navbar,
.footer {
  padding: 0 20px;
}

@media (max-width: 700px) {
  .navbar ul,
  .footer ul {
    flex-direction: column;
    height: auto;
  }
  .navbar li,
  .footer li {
    margin-bottom: 6px;
  }
  .navbar a,
  .footer a {
    font-size: 14px;
    padding: 8px 0;
  }
}
select {
  background: transparent;
  color: rgb(40, 5, 166);
  border: 1px solid white;
}
</style>
