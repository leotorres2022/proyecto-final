<template>
  <div class="carrito-container">
    <h1>Carrito de Compras</h1>

    <div v-if="carritoStore.items.length === 0" class="carrito-vacio">
      <p>Tu carrito está vacío</p>
      <router-link :to="{ name: 'tienda' }" class="btn-volver">
        Volver a la tienda
      </router-link>
    </div>

    <div v-else class="carrito-contenido">
      <div class="items">
        <div v-for="item in carritoStore.items" :key="item.idCarrito" class="item-carrito">
          <div class="item-info">
            <h3>{{ item.descripcion }}</h3>
            <p><strong>Categoría:</strong> {{ item.categoria }}</p>
            <p><strong>Talle:</strong> {{ item.talle?.nombre || item.talle }}</p>
            <p><strong>Socio:</strong> {{ item.socio?.nombre || item.socio }}</p>
            <p><strong>Cantidad:</strong> {{ item.cantidad }}</p>
            <p><strong>Precio unitario:</strong> ${{ item.precio }}</p>
            <p class="subtotal">
              <strong>Subtotal:</strong> ${{ (Number(item.precio) * Number(item.cantidad)).toLocaleString() }}
            </p>
          </div>
          <button @click="eliminarItem(item.idCarrito)" class="btn-eliminar">
            Eliminar
          </button>
        </div>
      </div>

      <div class="resumen">
        <h2>Resumen</h2>
        <p class="cantidad-items">
          Cantidad de items: {{ carritoStore.obtenerCantidadItems() }}
        </p>
        <p class="total">
          <strong>Total:</strong> ${{ carritoStore.obtenerTotal().toLocaleString() }}
        </p>
        <div class="botones">
          <button @click="comprar" class="btn-comprar">Comprar</button>
          <router-link :to="{ name: 'tienda' }" class="btn-seguir">
            Seguir comprando
          </router-link>
          <button @click="vaciarCarrito" class="btn-vaciar">Vaciar carrito</button>
        </div>
      </div>
    </div>

    <div class="volver">
      <router-link :to="{ name: 'tienda' }">
        <i class="pi pi-arrow-circle-left" style="font-size: 2rem"></i>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import useCarritoStore from '@/stores/carrito'
import 'primeicons/primeicons.css'

const router = useRouter()
const carritoStore = useCarritoStore()

carritoStore.cargarCarrito()

const eliminarItem = (id: string | undefined) => {
  if (confirm('¿Estás seguro de que quieres eliminar este item?')) {
    carritoStore.eliminarDelCarrito(id)
  }
}

const vaciarCarrito = () => {
  if (confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
    carritoStore.limpiarCarrito()
  }
}

const comprar = async () => {
  try {
    await carritoStore.crearComprasDelCarrito()
    alert('¡Compra realizada exitosamente!')
    router.push({ name: 'tienda' })
  } catch (error: any) {
    const mensaje = error.response?.data 
      ? JSON.stringify(error.response.data) 
      : 'Error al procesar la compra'
    alert('Error: ' + mensaje)
  }
}
</script>

<style scoped>
.carrito-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.carrito-vacio {
  text-align: center;
  padding: 3rem;
  background-color: #f0f0f0;
  border-radius: 12px;
}

.carrito-vacio p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.carrito-contenido {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.item-carrito {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-info {
  flex: 1;
}

.item-info h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.item-info p {
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.95rem;
}

.subtotal {
  margin-top: 1rem;
  font-size: 1.1rem;
  color: #169d3e;
  font-weight: bold;
}

.btn-eliminar {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-eliminar:hover {
  background-color: #c0392b;
}

.resumen {
  background-color: #f9f9f9;
  border: 2px solid #169d3e;
  border-radius: 12px;
  padding: 2rem;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.resumen h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  text-align: center;
}

.cantidad-items,
.total {
  font-size: 1rem;
  color: #666;
  margin: 1rem 0;
  text-align: center;
}

.total {
  font-size: 1.3rem;
  color: #169d3e;
  font-weight: bold;
  border-top: 2px solid #ddd;
  padding-top: 1rem;
  margin-top: 1.5rem;
}

.botones {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-comprar,
.btn-seguir,
.btn-vaciar {
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: block;
  text-align: center;
  font-weight: bold;
}

.btn-comprar {
  background-color: #169d3e;
  color: white;
}

.btn-comprar:hover {
  background-color: #0e7a2a;
}

.btn-seguir {
  background-color: #3498db;
  color: white;
}

.btn-seguir:hover {
  background-color: #2980b9;
}

.btn-vaciar {
  background-color: #95a5a6;
  color: white;
}

.btn-vaciar:hover {
  background-color: #7f8c8d;
}

.btn-volver {
  display: inline-block;
  background-color: #3498db;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.btn-volver:hover {
  background-color: #2980b9;
}

.volver {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
}

.volver a {
  color: #169d3e;
  cursor: pointer;
  transition: color 0.3s;
}

.volver a:hover {
  color: #0e7a2a;
}

@media (max-width: 768px) {
  .carrito-contenido {
    grid-template-columns: 1fr;
  }

  .resumen {
    position: relative;
    top: 0;
  }
}
</style>
