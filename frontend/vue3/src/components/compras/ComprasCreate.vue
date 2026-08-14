<template>
  <div>
    <form @submit.prevent="crear">
      <div >
      <label>Nombre de Socio</label>
       <p class="socio-logueado">
            {{ typeof compra.socio === 'object' ? compra.socio?.nombre : 'Buscando perfil de socio...' }}
        </p>
        <label for="" >Descripcion del Articulo</label>
        <p >{{ compra.descripcion }}</p>
        <label for="" >Precio</label>
          <p >{{ compra.precio }}</p>
          
         <label for="">Stock disponible</label>
        <p v-if="stockDisponible <= 0">  Sin stock disponible</p>
<p v-else>
  Stock disponible: {{ stockDisponible }}
</p>

          

        <label for="" >cantidad</label>
        <input type="number" name="" v-model="compra.cantidad"   min="1"  :max="stockDisponible">
        <label for="" >Talle</label>
         <select v-model="compra.talle" required>
        <option v-for="talle in talles" :key="talle.id" :value="talle">
          {{ talle.nombre }}
        </option>
       </select>
        <label for="" >Categoria</label>
       <p>{{ typeof compra.categoria === 'object' ? compra.categoria?.nombre : (compra.categoria || 'Sin categoría') }}</p>
       </div>
      
      <button type="submit">Crear</button>
    </form>

  </div>
<div class="volver" >
          <router-link :to="{name:'tienda'}"><i class="pi pi-arrow-circle-left" style="font-size: 2rem"></i></router-link>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, toRefs, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import UseComprasStore from '../../stores/compras'
import UseTallesStore from '../../stores/talles'
import UseSociosStore from '../../stores/socios'
import UseCategoriasStore from '../../stores/categorias'
import UseCarritoStore from '../../stores/carrito'
import UseProductosStore from '../../stores/producto'
import { useAuthStore } from '@/stores/auth'
import type { Compras } from '@/interfaces/Compras'
import ApiService from '@/services/ApiService'

const authStore = useAuthStore()
const socioLogueado = computed(() => authStore.user)

const router = useRouter()
const tallesStore = UseTallesStore()
const sociosStore = UseSociosStore()
const categoriasStore = UseCategoriasStore()
const productosStore = UseProductosStore()
const comprasStore = UseComprasStore()
const carritoStore = UseCarritoStore()

const { talles } = toRefs(tallesStore)
const { socios } = toRefs(sociosStore)
const { categorias } = toRefs(categoriasStore)
const { productos } = toRefs(productosStore)
const { compra } = toRefs(comprasStore)

const { getAll: getAllTalles } = tallesStore
const { getAll: getAllSocios } = sociosStore
const { getAll: getAllCategorias } = categoriasStore
const { getAll: getAllProductos } = productosStore
const { create } = comprasStore


const limpiar = () => {
  compra.value.cantidad = 1
  compra.value.talle = undefined
}


const stockDisponible = ref(0)


watch(
  [() => compra.value.producto, () => compra.value.talle],
  async ([nuevoProducto, nuevoTalle]) => {
    console.log("Producto:", nuevoProducto)
    console.log("Talle:", nuevoTalle)
        if (nuevoProducto && nuevoTalle) {
      try {
        const productoId =
          typeof nuevoProducto === 'object'
            ? nuevoProducto.id
            : nuevoProducto

        const talleId =
          typeof nuevoTalle === 'object'
            ? nuevoTalle.id
            : nuevoTalle

        console.log("productoId:", productoId)
        console.log("talleId:", talleId)

        const url = `api/tallestock/${productoId}/${talleId}/`

        console.log("URL:", url)

        const response = await (ApiService as any).get(  `api/tallestock/${productoId}/${talleId}/`)

        console.log("Respuesta stock:", response)

        stockDisponible.value = response?.stock ?? 0

            console.log( "Stock disponible:",     stockDisponible.value      )

            
        } catch (error) {
        console.error("Error al consultar stock:", error)
        stockDisponible.value = 0
      }
    } else {
      stockDisponible.value = 0
    }
  },
  { immediate: true }
)

onMounted(async () => {
  await getAllTalles()
  await getAllSocios()
  await getAllCategorias()
  await getAllProductos()
  carritoStore.cargarCarrito()

  limpiar()

  if (authStore.user && socios.value.length > 0) {
    const socioEncontrado = socios.value.find(
      (s) => s.dni === authStore.user.username || s.email === authStore.user.email
    )

    if (socioEncontrado) {
      compra.value.socio = socioEncontrado
    }
  }
})

const crear = async () => {
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
  if (Number(item.cantidad) > stockDisponible.value) {
  return alert(
    `La cantidad supera el stock disponible. Stock disponible: ${stockDisponible.value}`
  );
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
  if (!item.producto) {
    return alert('Debe seleccionar un producto');
  }

  const articulo_json = {
    descripcion: item.descripcion,
    precio: Number(item.precio),
    cantidad: Number(item.cantidad),
    producto: item.producto,
    talle: typeof item.talle === 'object' ? item.talle?.id : item.talle,
    categoria: typeof item.categoria === 'object' ? item.categoria?.id : item.categoria,
    socio: typeof item.socio === 'object' ? item.socio?.id : item.socio,
    estado: item.estado ?? 'pendiente',
  };

  console.log('Enviando a carrito:', articulo_json);
  console.log("========== VENTA ==========")
console.log("Producto:", item.producto)
console.log("Talle:", item.talle)
console.log("Cantidad vendida:", item.cantidad)
console.log("Stock antes:", stockDisponible.value)

  try {
    carritoStore.agregarAlCarrito(articulo_json as Compras);
    alert('Producto agregado al carrito');
    router.push({ name: 'carrito' });
    console.log("✅ Venta guardada")
console.log("Stock que debería quedar:",
  stockDisponible.value - Number(item.cantidad)
)
  } catch (error: any) {
    console.error("❌ ERROR AL GUARDAR COMPRA")
    console.error("Status:", error.response?.status)
    console.error("Respuesta backend:", error.response?.data)
    console.error("Error completo:", error)
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


