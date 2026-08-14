<template>
  <h1 class="titulo">Lista de Compras</h1>
  <table>
    <thead>
      <tr>
        
        <th>Socio</th>
        <th>Precio Final</th>
        <th>Fecha</th>
        <th>Estado</th>
        <th>Detalles</th>
        </tr>
    </thead>
    <tbody>
<tr v-for="compra in compras" :key="compra.id">
  <td>{{ typeof compra.socio === 'object' ? compra.socio?.nombre : (compra.socio || 'Sin nombre') }}</td>
  <td>{{ compra.total }}</td>
  <td>{{ formatoFecha(compra.fecha) }}</td>
  <td>{{ compra.estado }}</td>
  <td>
      <router-link :to="{ name: 'compras_show', params: { id: compra.id } }">
    <i class="pi pi-eye" style="font-size: 1.5rem"></i>
  </router-link>
 
      <router-link :to="{ name: 'compras_update', params: { id: compra.id } }">
    <i class="pi pi-pencil" style="font-size: 1.5rem"></i>
  </router-link>
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

const formatoFecha = (fecha: string | undefined) => {
  if (!fecha) return 'Sin fecha'
  return fecha.slice(0, 10)
}

const getClaseEstado = (estado: string) => {
  if (!estado) return '';
  const e = estado.toString();
  if (e === 'pendiente') return 'texto-amarillo';
  if (e === 'finalizada') return 'texto-verde';
  if (e === 'cancelada') return 'texto-rojo';
  return '';
};


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
.texto-verde {
  color: #28a745 !important;
}
.texto-rojo {
  color: #dc3545 !important;
}
.texto-amarillo {
  color: #ffc107 !important;
}
</style>
