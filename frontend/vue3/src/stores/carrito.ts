import { defineStore } from "pinia"
import { ref } from "vue"
import ApiService from "@/services/ApiService"
import type { Compras } from "@/interfaces/Compras"
import type { Socios } from "@/interfaces/Socios"
import type { Talles } from "@/interfaces/Talles"
import type { Categorias } from "@/interfaces/Categorias"
import type { Producto } from "@/interfaces/Producto"

export interface ItemCarrito {
  idCarrito: string // ID temporal 
  descripcion: string
  precio: number
  cantidad: number
  producto?: Producto | number
  talle?: Talles | number
  categoria?: Categorias | number
  socio?: Socios | number
  estado?: 'pendiente' | 'finalizada' | 'cancelada' 
}

const useCarritoStore = defineStore('carrito', () => {
  const items = ref<Array<ItemCarrito>>([])
  const url = 'api/compras'

  // Cargar carrito desde localStorage
  const cargarCarrito = () => {
    const carritoGuardado = localStorage.getItem('carrito')
    if (carritoGuardado) {
      items.value = JSON.parse(carritoGuardado)
    }
  }

  // Guardar carrito en localStorage
  const guardarCarrito = () => {
    localStorage.setItem('carrito', JSON.stringify(items.value))
  }

  // Agregar item al carrito
  const agregarAlCarrito = (compra: Compras) => {
    const itemConId: ItemCarrito = {
      idCarrito: Date.now().toString(), // ID temporal único
      descripcion: compra.descripcion ?? '',
      precio: compra.precio ?? 0,
      cantidad: compra.cantidad ?? 1,
      producto: compra.producto,
      talle: compra.talle,
      categoria: compra.categoria,
      socio: compra.socio
    }
    items.value.push(itemConId)
    guardarCarrito()
  }

  // Eliminar item del carrito
  const eliminarDelCarrito = (idItem: string | undefined) => {
    if (idItem) {
      items.value = items.value.filter(item => item.idCarrito !== idItem)
      guardarCarrito()
    }
  }

  // Limpiar carrito
  const limpiarCarrito = () => {
    items.value = []
    localStorage.removeItem('carrito')
  }

  // Crear una sola compra con todos los ítems del carrito

const crearComprasDelCarrito = async () => {
  if (items.value.length === 0) {
    throw new Error('El carrito está vacío')
  }

  const primerItem = items.value[0]!

  const socio_id = typeof primerItem.socio === 'object'
    ? primerItem.socio?.id
    : primerItem.socio

  if (!socio_id) {
    throw new Error('No hay socio válido para la compra')
  }

  const detalles = items.value.map(item => {

    // ==============================
    // VALIDAR PRODUCTO
    // ==============================

    if (!item.producto) {
      throw new Error('Todos los ítems deben incluir un producto')
    }

    const producto_id = typeof item.producto === 'object'
      ? item.producto?.id
      : item.producto

    // ==============================
    // OBTENER TALLE
    // ==============================

    const talle_id = typeof item.talle === 'object'
      ? item.talle?.id
      : item.talle

    if (!talle_id) {
      throw new Error(
        `El producto ${producto_id} no tiene un talle válido`
      )
    }

    // ==============================
    // CANTIDAD
    // ==============================

    const cantidad = Number(item.cantidad)

    if (cantidad <= 0) {
      throw new Error(
        `La cantidad del producto ${producto_id} debe ser mayor a 0`
      )
    }

    // ==============================
    // MOSTRAR EN CONSOLA
    // ==============================

    console.log('========== DETALLE VENTA ==========')
    console.log('Producto ID:', producto_id)
    console.log('Talle ID:', talle_id)
    console.log('Cantidad:', cantidad)
    console.log('Precio:', Number(item.precio))

    return {
      producto_id,
      talle_id,
      cantidad,
      precio_unitario: Number(item.precio)
    }
  })

  const compraData = {
    socio_id,

    total: items.value.reduce(
      (sum, item) =>
        sum + Number(item.precio) * Number(item.cantidad),
      0
    ),

    estado: primerItem.estado ?? 'pendiente',

    detalles
  }

  // ==============================
  // VER DATOS QUE SE ENVÍAN
  // ==============================

  console.log('========== COMPRA ==========')
  console.log(
    'Datos enviados al backend:',
    JSON.stringify(compraData, null, 2)
  )

  try {

    const response = await ApiService.create(
      url + '/',
      compraData
    )

    console.log('✅ COMPRA GUARDADA')
    console.log('Respuesta backend:', response.data)

    limpiarCarrito()

    return true

  } catch (error: any) {

    console.error('❌ ERROR AL CREAR COMPRA')
    console.error('Status:', error.response?.status)
    console.error(
      'Respuesta backend:',
      error.response?.data
    )
    console.error('Error completo:', error)

    throw error
  }
}
  // Obtener total del carrito
  const obtenerTotal = () => {
    return items.value.reduce((total, item) => {
      return total + (Number(item.precio) * Number(item.cantidad))
    }, 0)
  }

  // Obtener cantidad de items
  const obtenerCantidadItems = () => {
    return items.value.length
  }

  return {
    items,
    agregarAlCarrito,
    eliminarDelCarrito,
    limpiarCarrito,
    crearComprasDelCarrito,
    obtenerTotal,
    obtenerCantidadItems,
    cargarCarrito,
    guardarCarrito
  }
})

export default useCarritoStore
