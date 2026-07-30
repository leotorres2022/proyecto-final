<template>
  <div>
    <form @submit.prevent="crear">
      <div >
      <label>Nombre de Socio</label>
       <p class="socio-logueado">
            {{ compra.socio?.nombre || 'Buscando perfil de socio...' }}
        </p>
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
       <p>{{ compra.categoria }}</p>
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
import UseCarritoStore from '../../stores/carrito'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
const authStore = useAuthStore()
const socioLogueado = computed(() => {
  return authStore.user; 
})
import { useRouter } from 'vue-router'

const router = useRouter()
const limpiar = () => {
  compra.value.cantidad = 1
  compra.value.talle = undefined
 }

const tallesStore = UseTallesStore()
const sociosStore = UseSociosStore()
const categoriasStore = UseCategoriasStore()
const comprasStore = UseComprasStore()
const carritoStore = UseCarritoStore()

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
carritoStore.cargarCarrito()

limpiar()
if (authStore.user && socios.value.length > 0) {
    const socioEncontrado = socios.value.find(
      (s) => s.dni === authStore.user.username || s.email === authStore.user.email
    )

    if (socioEncontrado) {
      // Guardamos el objeto socio completo en la compra para que el formulario y el submit lo utilicen
      compra.value.socio = socioEncontrado
    }
  }

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

  // Buscar el ID de la categoría por nombre
  const categoriaBuscada = categorias.value.find(
    (cat) => cat.nombre === item.categoria
  );

  if (!categoriaBuscada) {
    return alert('Categoría no encontrada: ' + item.categoria);
  }

  const articulo_json = {
    descripcion: item.descripcion,
    precio: Number(item.precio) ,
    cantidad: Number(item.cantidad),
    talle: item.talle.id || item.talle,
    categoria: categoriaBuscada.id,
    socio: item.socio.id,
    estado:item.estado ?? 'pendiente' ,// Agregamos el estado por defecto
    
  };

  console.log('Enviando a carrito:', articulo_json);

  try {
    carritoStore.agregarAlCarrito(articulo_json as Compras);
    alert('Producto agregado al carrito');
    router.push({ name: 'carrito' });
    
  } catch (error: any) {
    console.error('Error detallado:', error.response?.data || error);
    const mensaje = error.response?.data 
      ? JSON.stringify(error.response.data) 
      : 'Error al agregar al carrito';
    alert('Error: ' + mensaje);
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


