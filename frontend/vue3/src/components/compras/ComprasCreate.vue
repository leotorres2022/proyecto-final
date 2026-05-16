<template>
  <div>
    <form @submit.prevent="crear">
      <div >
       <label>Nombre de Socio</label>
          <select v-model="compra.socio" required>
         <option v-for="socio in socios" :key="socio.id" :value="socio">
         {{ socio.nombre }}
         </option>
        </select>
        <label for="" >Descripcion del Articulo</label>
        <p >{{ compra.descripcion }}</p>
        <label for="" >Precio</label>
          <p >{{ compra.precio }}</p>
        <label for="" >cantidad</label>
        <input type="text" name="" v-model="compra.cantidad">
        <label for="" >Talle</label>
         <select v-model="compra.talle" required>
        <option v-for="talle in talles" :key="talle.id" :value="talle">
          {{ talle.nombre }}
        </option>
       </select>
        <label for="" >Categoria</label>
      <select v-model="compra.categoria" required>
        <option v-for="categoria in categorias" :key="categoria.id" :value="categoria">
          {{ categoria.nombre }}
        </option>
      </select> 
       </div>
      <button type="submit">Crear</button>
    </form>

  </div>
<div class="volver" >
          <router-link :to="{name:'tienda'}"><i class="pi pi-arrow-circle-left" style="font-size: 2rem"></i></router-link>
    </div>
</template>

<script setup lang="ts">
import { toRefs} from 'vue'
import UseComprasStore from '../../stores/compras'
import UseTallesStore from '../../stores/talles'
import UseSociosStore from '../../stores/socios'
import  UseCategoriasStore from '../../stores/categorias'
const limpiar = () => {
  compra.value.cantidad = 1
  compra.value.talle = undefined
  compra.value.categoria = undefined
  compra.value.socio = undefined
}

const tallesStore = UseTallesStore()
const sociosStore = UseSociosStore()
const categoriasStore = UseCategoriasStore()
const comprasStore = UseComprasStore()

const { talles } = toRefs(tallesStore)
const { socios } = toRefs(sociosStore)
const { categorias } = toRefs(categoriasStore)
const { compra } = toRefs(comprasStore)

const { getAll: getAllTalles } = tallesStore
const { getAll: getAllSocios } = sociosStore
const { getAll: getAllCategorias } = categoriasStore
const { create } = comprasStore



import { onMounted } from 'vue'
import type { Compras } from '@/interfaces/Compras'
onMounted(async () => {
await getAllTalles()
await getAllSocios()
await getAllCategorias()

limpiar()

})

const crear = async () => {
  // 1. Validaciones locales para evitar tocar el store prematuramente
  const item = compra.value;

  if (!item.descripcion?.trim()) {
    return alert('La descripción es obligatoria');
  }
  if (Number(item.precio) <= 0) {
    return alert('El precio debe ser mayor a 0');
  }
  if (Number(item.cantidad) <= 0) {
    return alert('La cantidad debe ser mayor a 0');
  }
  if (!item.talle) {
    return alert('Debe seleccionar un Talle');
  }
  if (!item.categoria) {
    return alert('Debe seleccionar una categoría');
  }
  if (!item.socio) {
    return alert('Debe seleccionar un Socio');
  }


  const articulo_json = {
    descripcion: item.descripcion,
    precio: Number(item.precio) * Number(item.cantidad),
    cantidad: Number(item.cantidad),
    talle: item.talle.id || item.talle,
    categoria: item.categoria.id || item.categoria,
    socio: item.socio.id || item.socio,
  };

  console.log('Enviando a Django:', articulo_json);

  try {
    // Usamos "as any" para que TypeScript no se queje de que falta el objeto completo
    await create(articulo_json as any);
    
    alert('Compra creada correctamente');
    
    // 3. Resetear el store correctamente
    limpiarFormulario();
    
  } catch (error: any) {
    console.error('Error detallado:', error.response?.data || error);
    const mensaje = error.response?.data 
      ? JSON.stringify(error.response.data) 
      : 'Error de conexión con el servidor';
    alert('Error al crear compra: ' + mensaje);
  }
}

const limpiarFormulario = () => {
  compra.value = {
    descripcion: '',
    precio: 0,
    cantidad: 0,
    talle: undefined,
    categoria: undefined,
    socio: undefined
  };
}

</script>

<style scoped>
form {
  background-color: #fff;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  margin: auto;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

label {
  display: block;
  margin-top: 1rem;
  font-weight: bold;
  color: #333;
  font-size: 1rem;
}

select,
input[type="text"] {
  width: 100%;
  padding: 0.75rem 1rem;
  margin-top: 0.3rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

select:focus,
input[type="text"]:focus {
  border-color: #169d3e;
  outline: none;
}

p {
  background-color: #f0f0f0;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 1rem;
  color: #444;
  margin-top: 0.3rem;
  margin-bottom: 1rem;
}




.volver{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
}

</style>


