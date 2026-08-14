
import { defineStore } from "pinia"
import { ref } from "vue"
import ApiService from "@/services/ApiService"
import type  {Socios}   from '@/interfaces/Socios'
import type {Talles} from '@/interfaces/Talles'
import type {Compras} from '@/interfaces/Compras'
import type { Categorias } from "@/interfaces/Categorias"
import type { Producto } from '@/interfaces/Producto'

const useComprasStore = defineStore('compras', () => {
  const compras = ref<Array<Compras>>([])
  const compra = ref<Compras>({
    id: 0,
    descripcion: '',
    precio: 0,
    cantidad: 0,
    talle: {} as Talles,
    categoria: {} as Categorias,
    socio: {} as Socios,
    estado: 'pendiente' // Valor por defecto para el estado
  })
const url = 'api/compras'
  async function getAll()
  {
    const data = await ApiService.getAll(url)
    if (data) {
      compras.value = data
       console.log('Compras cargadas:', data)
              }
  }
  async function create(compra: Compras) {
    const response = await ApiService.create(url+'/', compra)
    if (response) {
           return response
    }

  }



 async function update(compra: Compras) {
    if (compra.id) {
    const data = await ApiService.update(url + '/',compra.id, compra)
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

function seleccionarProducto(producto: Producto, categoria?: Categorias) {
  compra.value.descripcion = producto.nombre
  compra.value.precio = producto.precio
  compra.value.categoria = categoria ?? (producto.categoria as any)
  compra.value.producto = producto
}


return { compra, compras, getAll, destroy, create, update , seleccionarProducto  }

})




export default useComprasStore
