import { defineStore } from "pinia"
import { ref } from "vue"
import ApiService from "@/services/ApiService"
import type { Compras } from "@/interfaces/Compras"
import type { Socios } from "@/interfaces/Socios"
import type { Talles } from "@/interfaces/Talles"

export interface ItemCarrito {
  idCarrito: string // ID temporal único del item en carrito
  descripcion: string
  precio: number
  cantidad: number
  talle?: Talles
  categoria?: string
  socio?: Socios
  estado?: 'pendiente' | 'finalizada' | 'cancelada' // Nuevo campo para el estado de la compra
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
      descripcion: compra.descripcion,
      precio: compra.precio,
      cantidad: compra.cantidad,
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

  // Crear todas las compras del carrito
  const crearComprasDelCarrito = async () => {
    try {
      const promesas = items.value.map(item => {
        const compraData: Compras = {
          descripcion: item.descripcion,
          precio: item.precio * item.cantidad, // Multiplicar precio por cantidad
          cantidad: item.cantidad,
          talle: item.talle,
          categoria: item.categoria,
          socio: item.socio,
          estado: 'pendiente' ,// Establecer estado inicial como pendiente
          
        }
        return ApiService.create(url + '/', compraData)
      })
      
      await Promise.all(promesas)
      limpiarCarrito()
      return true
    } catch (error) {
      console.error('Error al crear compras:', error)
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
