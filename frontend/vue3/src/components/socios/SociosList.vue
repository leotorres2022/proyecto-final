<template>
    <h1 class="titulo">Listado de socios</h1>
  <div class="crear-container">

</div>
  <table>
    <thead>
      <tr>
        <th>id</th>
        <th>nombre</th>
        <th>direccion</th>
        <th>telefono</th>
        <th>DNI</th>
        <th>División</th>
        <th>email</th>
        <th>estado</th>
        </tr>
    </thead>
    <tbody>
      <tr v-for="socio in visibleSocios" :key="socio.id">
        <td>{{ socio.id }}</td>
        <td>{{ socio.nombre }}</td>
        <td>{{ socio.direccion }}</td>
        <td>{{ socio.telefono }}</td>
        <td>{{ socio.dni }}</td>
        <td>{{ socio.division }}</td>
        <td>{{ socio.email }}</td>
 <td :class="getClaseEstado(socio.estado)">
  {{ socio.estado }}
</td>
        
   <td v-if="userAuthStore.isAuthenticated && (userAuthStore.user?.groups?.includes('admin') || userAuthStore.user?.is_superuser)">
  
  <router-link :to="{ name: 'socios_update', params: { id: socio.id } }">
    <i class="pi pi-pencil" style="font-size: 1.5rem"></i>
  </router-link>

  <router-link :to="{ name: 'socios_show', params: { id: socio.id } }">
    <i class="pi pi-eye" style="font-size: 1.5rem"></i>
  </router-link>

  <button @click.prevent="eliminar(socio.id as number)">
    <i class="pi pi-trash" style="font-size: 1.5rem"></i>
  </button>

</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { computed, onMounted, toRefs } from 'vue'
import useSociosStore from '../../stores/socios'
import { useAuthStore } from '@/stores/auth';
const sociosStore = useSociosStore()
const { socios } = toRefs(sociosStore)
const { getAll, destroy } = sociosStore
const userAuthStore = useAuthStore()

const visibleSocios = computed(() => {
  const username = userAuthStore.user?.username
  if (userAuthStore.isAuthenticated && username) {
    const socioEncontrado = socios.value.find((s) => s.dni === username)
    if (socioEncontrado) {
      return [socioEncontrado]
    }
  }
  return socios.value
})

onMounted(async () => {
  await getAll()
})
async function eliminar(id: number) {
  if (confirm('¿Estás seguro de eliminar el socio ' + id + '?')) {
    await destroy(id)
    await getAll()
  }
}

const getClaseEstado = (estado: string) => {
  if (!estado) return '';
  const e = estado.toString();
  if (e === 'Activo') return 'texto-verde';
  if (e === 'Moroso') return 'texto-rojo';
  if (e === 'Pendiente') return 'texto-amarillo';
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
