
import { defineStore } from "pinia"
import { ref } from "vue"
import ApiService from "@/services/ApiService"
import type  {Producto}   from '@/interfaces/Producto'

const useProductosStore = defineStore('productos', () => {
  const productos = ref<Array<Producto>>([])
  const producto= ref<Producto>({
   id: 0, 
   nombre: '',
    precio: 0,
   stock: 0,
   categoria: 0
  })
const url = 'api/productos'
  async function getAll()
  {
    const data = await ApiService.getAll(url)
    if (data) {
      productos.value = data
              }
  }
  async function create(producto:Producto) {
    const response = await ApiService.create(url, producto )
    if (response) {
           return response
    }

  }

 async function update(producto: Producto) {
    if (producto.id) {
    const data = await ApiService.update(url +'/',producto.id, producto)
    if (data) {
      return data
    }
  }
  }

  async function destroy(id: number) {
    const data = await ApiService.destroy(url + '/', id)
    if (data) {
      return data
          }
  }
return { productos, producto, getAll, destroy, create, update }

})

export default useProductosStore    
