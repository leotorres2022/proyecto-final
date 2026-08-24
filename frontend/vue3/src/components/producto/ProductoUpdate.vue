<template>
  <div>
    <form @submit.prevent="editar">

      <div class="detalle-socio">
        <label>Nombre</label>
        <input
          type="text"
          v-model="producto.nombre"
          class="input"
        >
        <label>Precio</label>
        <input
          type="number"
          step="0.01"
          v-model="producto.precio"
          class="input"
        >
        <label>Categoría</label>
        <input
          type="number"
          v-model="producto.categoria"
          class="input"
        >
        <label>Imagen</label>
        <input
          type="file"
          accept="image/*"
          @change="seleccionarImagen"
          class="input"
        >
        <div v-if="producto.imagen" class="imagen-actual">
          <p>Imagen actual:</p>
          <img
            :src="producto.imagen"
            :alt="producto.nombre"
          >
        </div>
      </div>
      <button type="submit" class="modificar">
        Modificar Producto
      </button>
    </form>
  </div>

  <div class="volver">
    <router-link :to="{ name: 'productos_list' }">
      <i    class="pi pi-arrow-circle-left"   style="font-size: 2rem"></i>
    </router-link>
  </div>
</template>

<script setup lang="ts">

import { ref, toRefs, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import UseProductosStore from '../../stores/producto'
const route = useRoute()
const productosStore = UseProductosStore()
const { producto, productos } = toRefs(productosStore)
const imagenArchivo = ref<File | null>(null)

  onMounted(() => {
  const id = Number(route.params.id)
  const encontrado = productos.value.find(
    p => p.id === id
  )

  if (encontrado) {
    producto.value = { ...encontrado }
  }

})

const seleccionarImagen = (event: Event) => {

  const input = event.target as HTMLInputElement

  if (input.files && input.files.length > 0) {
    const archivo = input.files[0]
    if (archivo) {
      imagenArchivo.value = archivo
    }
  }

}

const editar = async () => {

  if (!producto.value.nombre) {
    alert('El nombre es obligatorio')
    return
  }

  if (producto.value.precio <= 0) {
    alert('El precio debe ser mayor a 0')
    return
  }

  if (!producto.value.categoria) {
    alert('La categoría es obligatoria')
    return
  }

  try {
  await productosStore.update(producto.value)

  alert('Producto actualizado correctamente')

} catch (error: any) {
  console.error('ERROR COMPLETO:', error)
  console.error('RESPUESTA DJANGO:', error.response?.data)

  alert(
    JSON.stringify(
      error.response?.data || error.message
    )
  )
}

}

</script>

<style scoped>

.detalle-socio {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  color: #333;
  font-family: 'Segoe UI', sans-serif;
  font-size: 1.3rem;
}

.detalle-socio label {
  display: block;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.input {
  width: 100%;
  padding: 0.7rem;
  box-sizing: border-box;
  font-size: 1rem;
}

.imagen-actual {
  margin-top: 1rem;
}

.imagen-actual img {
  max-width: 200px;
  max-height: 200px;
  object-fit: contain;
}

.modificar {
  display: block;
  width: 20%;
  padding: 0.6rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
  margin: 1rem auto;
}

.volver {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
}

</style>
