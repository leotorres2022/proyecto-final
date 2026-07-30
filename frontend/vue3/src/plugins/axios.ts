import axios from 'axios'
export const instance = axios.create({
  baseURL: 'http://localhost:8000/',
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

