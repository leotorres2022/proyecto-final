<template>
  <h1 class="titulo">Lista de Compras</h1>
  <table>
    <thead>
      <tr>
        <th>id</th>
        <th>Descripcion</th>
        <th>Precio Final</th>
        <th>Cantidad</th>
        <th>Talle</th>
        <th>Categoria</th>
        <th>Socio</th>
        <th v-if="userStore.modo === 'admin'" >Acciones</th>
      </tr>
    </thead>
    <tbody>
<tr v-for="compra in compras" :key="compra.id">
  <td>{{ compra.id }}</td>
  <td>{{ compra.descripcion }}</td>
  <td>{{ compra.precio }}</td>
  <td>{{ compra.cantidad }}</td>
  
  <!-- Cambiamos .talle?.nombre por .talle_detalle -->
  <td>{{ compra.talle|| 'Sin talle' }}</td>
  
  <!-- Cambiamos .categoria?.nombre por .categoria_detalle -->
  <td>{{ compra.categoria|| 'Sin categoria' }}</td>
  
  <!-- Cambiamos .socio?.nombre por .socio_detalle -->
  <td>{{ compra.socio || 'Sin nombre' }}</td>

  <!-- Resto de tus acciones (pencil, eye, trash) -->
  <td v-if="userStore.modo === 'admin'">
     <!-- Tus botones aquí... -->
  </td>
</tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { onMounted, toRefs } from 'vue'
import useComprasStore from '../../stores/compras'
import useTallesStore from '../../stores/talles'
import useSociosStore from '../../stores/socios'
import useCategoriasStore from '../../stores/categorias'
import useUserStore from '@/stores/user'
const userStore = useUserStore()

const comprasStore = useComprasStore()
const { compras } = toRefs(comprasStore)
const { getAll, destroy } = comprasStore
const { getAll: getAllSocios } = useSociosStore()
const { getAll: getAllTalles } = useTallesStore()
const { getAll: getAllCategorias } = useCategoriasStore()


onMounted(async () => {
  await getAllTalles()
  await getAllCategorias()
  await getAllSocios()
  await getAll()

})

async function eliminar(id: number) {
  if (confirm('¿Estás seguro de eliminar esta compra ' + id + '?')) {
    await destroy(id)
    await getAll()
  }
}


</script>

<style scoped>
.titulo {
  text-align: center;
  margin-top: 1rem;
}
.crear-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 2rem;
  font-family: 'Segoe UI', sans-serif;
  font-size: 1.3rem;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

thead th {
  background-color: #007BFF;
  color: white;
  padding: 1rem;
  text-align: left;
  font-weight: bold;
}

tbody td {
  padding: 1rem;
  border-top: 1px solid #eee;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

td i {
  margin-right: 10px;
  color: #555;
  cursor: pointer;
  transition: color 0.3s ease;
}

td i:hover {
  color: #007BFF;
}
td ul {
  list-style-type: none; /* Elimina los puntos */
  padding-left: 0;       /* Elimina el sangrado izquierdo */
  margin: 0;
}
.pi-pencil
{
  cursor: pointer;
  color: #e5f41b;
}
</style>
