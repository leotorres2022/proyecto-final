<template>
  <div>
    <form @submit.prevent="crear">

      <div>
        <label>Nombre del Producto</label>
        <input
          type="text"
          v-model="producto.nombre"
        >
      </div>

      <div>
        <label>Precio</label>
        <input
          type="number"
          v-model="producto.precio"
        >
      </div>
      <label>Categoria</label>
<select v-model="producto.categoria" required>
  <option disabled value="">Seleccioná una categoría</option>

  <option
    v-for="categoria in categorias"
    :key="categoria.id"
    :value="categoria.id"
  >
    {{ categoria.nombre }}
  </option>
</select>

      <div>
        <label>Imagen</label>
        <input
          type="file"
          @change="seleccionarImagen"
        >
      </div>

      <button type="submit">
        Crear Producto
      </button>

    </form>
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
import  UseProductoStore from '../../stores/producto'
import { ref } from 'vue'
import  useCategoriasStore  from '@/stores/categorias'

const productoStore = UseProductoStore()
const categoriasStore = useCategoriasStore()
const { categorias } = toRefs(categoriasStore)  
const { producto } = toRefs(productoStore)
const { getAll: getAllCategorias } = categoriasStore

const imagenArchivo = ref<File | null>(null)

const limpiarFormulario = () => {
  producto.value = {
    id: 0,
    nombre: '',
    precio: 0,
    categoria: 0,
    imagen: null
  }
   imagenArchivo.value = null
}

onMounted(() => {
  limpiarFormulario()
  getAllCategorias()
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

const crear = async () => {

  if (!producto.value.nombre) {
    alert('El nombre del producto es obligatorio')
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
    const response = await productoStore.create(
  producto.value,
  imagenArchivo.value
)

    console.log(response)

    alert('Producto creado correctamente')

    limpiarFormulario()

  } catch (error) {
    console.error(error)
    alert('Error al crear el producto')
  }
}
</script>

<style scoped>
form {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 0.8rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.volver{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
}


</style>
