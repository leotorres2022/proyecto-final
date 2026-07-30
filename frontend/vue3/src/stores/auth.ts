import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { instance as api } from '@/plugins/axios'

export const useAuthStore = defineStore('auth', () => {
  // 1. Cambiamos localStorage por sessionStorage para la inicialización
  const accessToken = ref<string | null>(localStorage.getItem('access') || null)
  const refreshToken = ref<string | null>(localStorage.getItem('refresh') || null)
  const user = ref<any>(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  async function loadUser() {
    if (!accessToken.value) return
    try {
      const response = await api.get('/api/auth/me/')
      user.value = response.data
    } catch (error) {
      console.error('Error cargando usuario:', error)
      user.value = null
    }
  }

  async function login(username: string, password: string) {
    const response = await api.post('/api/auth/token/', { username, password })

    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh

    // 2. Guardamos en sessionStorage al iniciar sesión
    localStorage.setItem('access', response.data.access)
    localStorage.setItem('refresh', response.data.refresh)

    // Cargar los datos del usuario después del login
    await loadUser()
  }

  async function logout() {
    try {
      // Llamar al endpoint de logout del backend
      await api.post('/api/auth/logout/', { refresh: refreshToken.value })
    } catch (error) {
      console.error('Error al cerrar sesión:', error)
    } finally {
      // Limpiar tokens del cliente de todas formas
      accessToken.value = null
      refreshToken.value = null
      user.value = null
      
      // 3. Eliminamos de sessionStorage al cerrar sesión manualmente
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    }
  }

  // Cargar el usuario si hay token al inicializar la app
  if (accessToken.value) {
    loadUser()
  }

  return { accessToken, refreshToken, user, isAuthenticated, login, logout, loadUser }
})