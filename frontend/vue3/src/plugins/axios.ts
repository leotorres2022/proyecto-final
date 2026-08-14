import axios from 'axios'
export const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 10000,
})
// Interceptor para agregar el token en los headers
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Interceptor de respuesta para intentar refrescar el token cuando el access expiró
instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    if (!originalRequest) return Promise.reject(error)

    const status = error.response ? error.response.status : null

    // Solo intentamos refresh una vez por request
    if (status === 401 && !originalRequest._retry) {
      const refresh = localStorage.getItem('refresh')
      if (!refresh) {
        return Promise.reject(error)
      }
      originalRequest._retry = true
      try {
        const resp = await instance.post('/api/auth/token/refresh/', { refresh })
        const newAccess = resp.data.access
        // Guardar nuevo access y actualizar headers
        localStorage.setItem('access', newAccess)
        instance.defaults.headers.Authorization = `Bearer ${newAccess}`
        originalRequest.headers = originalRequest.headers || {}
        originalRequest.headers.Authorization = `Bearer ${newAccess}`
        return instance(originalRequest)
      } catch (e) {
        // Si falla el refresh, limpiar tokens
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        return Promise.reject(e)
      }
    }

    return Promise.reject(error)
  }
)

