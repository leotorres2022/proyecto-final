<template>
  <div class="detalle-producto">
    <h2>
      <i class="pi pi-box" style="margin-right: 8px"></i>
      Detalle del Producto
    </h2>
    <p>
      <i class="pi pi-user" style="margin-right: 8px"></i>
      <strong>Nombre:</strong>
      <span class="dato">{{ producto.nombre }}</span>
    </p>
    <p>
      <i class="pi pi-hash" style="margin-right: 8px"></i>
      <strong>ID:</strong>
      <span class="dato">{{ producto.id }}</span>
    </p>
    <p>
      <i class="pi pi-dollar" style="margin-right: 8px"></i>
      <strong>Precio:</strong>
      <span class="dato">
        ${{ producto.precio.toLocaleString() }}
      </span>
    </p>
    <p>
      <i class="pi pi-tag" style="margin-right: 8px"></i>
      <strong>ID Categoría:</strong>
      <span class="dato">{{ producto.categoria }}</span>
    </p>
    <div v-if="producto.imagen">
      <strong>Imagen:</strong>
      <br>
      <img
        :src="producto.imagen"
        :alt="producto.nombre"
        style="max-width: 250px; margin-top: 10px;"
      >
    </div>
    <div v-else>
      <p>
        <strong>Imagen:</strong>
        Sin imagen disponible
      </p>
    </div>
  </div>
  <div class="volver">
    <router-link :to="{ name: 'productos_list' }">
      <i
        class="pi pi-arrow-circle-left"
        style="font-size: 2rem"
      ></i>
    </router-link>
  </div>
</template>

<script setup lang="ts">

import { toRefs, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import UseProductosStore from '../../stores/producto'

const route = useRoute()
const productosStore = UseProductosStore()
const { producto, productos } = toRefs(productosStore)
onMounted(async () => {
  const id = route.params.id
  console.log('ID del producto:', id)
  const encontrado = productos.value.find(
    producto => producto.id == parseInt(id as string)
  )

  producto.value = encontrado ?? {
    id: 0,
    nombre: '',
    precio: 0,
    categoria: 0,
    imagen: null
  }

})

</script>


<style scoped>

.detalle-producto {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  color: #333;
  font-family: 'Segoe UI', sans-serif;
}

.detalle-producto h2 {
  text-align: center;
  color: #444;
  margin-bottom: 1.5rem;
}

.detalle-producto p {
  margin: 1rem 0;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
}

.dato {
  margin-left: 8px;
  color: #007BFF;
  font-weight: bold;

}

.volver{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
}
</style>

