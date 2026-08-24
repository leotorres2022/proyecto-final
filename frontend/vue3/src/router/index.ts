import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import tienda_routes from './tienda_routes'
import categorias_routes from './categorias_routes'
import ConfiguracionesView from '@/views/ConfiguracionesView.vue'
import ClubView from '@/views/ClubView.vue'
import CarritoView from '@/views/CarritoView.vue'
import socios_routes from './socios_routes'
import galeria_routes from './galeria_routes'
import talles_routes from './talles_routes'
import compras_routes from './compras_routes'
import division_routes from './division_routes'
import LoginView from '@/views/LoginView.vue' 
import producto_routes from './producto_routes'
import  { useAuthStore } from '@/stores/auth' 



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      
    },
  ...tienda_routes,
  ...categorias_routes,
  ...socios_routes,
  ...galeria_routes,
  ...talles_routes,
  ...compras_routes,
  ...division_routes,
  ...producto_routes,
    { path: '/carrito', name: 'carrito', component: CarritoView },
    { path: '/configuraciones', name: 'configuraciones', component: ConfiguracionesView },
    { path: '/club', name: 'club', component: ClubView ,
      
    },
    { path: '/login', name: 'login', component: LoginView },
     
  ],
})
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Si la ruta requiere auth y no está autenticado, rebota al login
    next({ name: 'login' });
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    // Si ya está logueado e intenta ir al login, lo mandamos al home
    next({ name: 'home' });
  } else {
    next();
  }
});


export default router
