import { defineStore } from "pinia"
import { ref } from "vue"
import ApiService from "@/services/ApiService"
import type { Producto } from '@/interfaces/Producto'

const useProductosStore = defineStore('productos', () => {

  const productos = ref<Array<Producto>>([])

  const producto = ref<Producto>({
    id: 0,
    nombre: '',
    precio: 0,
    categoria: 0
  })

  const url = 'api/productos/'

  async function getAll() {
    const data = await ApiService.getAll(url)

    if (data) {
      productos.value = data
    }
  }

async function getStockTodos() {
  const data = await ApiService.getAll('api/tallestock/')

  if (data) {
    return data
  }
}

  async function create(producto: Producto, imagen: File | null) {

    const formData = new FormData()

    formData.append('nombre', producto.nombre)
    formData.append('precio', producto.precio.toString())
    formData.append('categoria', producto.categoria.toString())

    if (imagen) {
      formData.append('imagen', imagen)
    }

    const response = await ApiService.create(
      url,
      formData
    )

    if (response) {
      return response
    }
  }

  async function update(producto: Producto) {

    if (producto.id) {

      const datos = {
        nombre: producto.nombre,
        precio: producto.precio,
        categoria: producto.categoria
      }

      const data = await ApiService.update(
        url,
        producto.id,
        datos
      )

      if (data) {
        return data
      }
    }
  }

  async function destroy(id: number) {
    const data = await ApiService.destroy(url, id)

    if (data) {
      return data
    }
  }

  return {
    productos,
    producto,
    getAll,
    getStockTodos,
    destroy,
    create,
    update
  }
})

export default useProductosStore
