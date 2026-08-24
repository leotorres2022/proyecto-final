<template>
  <h1 class="titulo">Lista de Productos</h1>
    <div class="crear-container">
  <router-link :to="{name:'productos_create'}">CREAR</router-link>
   </div>
   <div class="volver" >
          <router-link :to="{name:'configuraciones'}"><i class="pi pi-arrow-circle-left" style="font-size: 2rem"></i></router-link>
  </div>
  <table>
    <thead>
      <tr>
        <th>id</th>
        <th>nombre</th>
        <th>categoria</th>
        <th>precio</th>
        <th>acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="producto in productos" :key="producto.id">
        <td>{{ producto.id }}</td>
        <td>{{ producto.nombre }}</td>
        <td> {{ producto.categoria }}</td>
        <td> {{ producto.precio }}</td>
        <td>
          <router-link :to="{name:'productos_update',params:{id:producto.id}}"><i class="pi pi-pencil" style="font-size: 1.5rem" ></i></router-link>
          <router-link :to="{name:'productos_show',params:{id:producto.id}}"><i class="pi pi-eye" style="font-size: 1.5rem"></i></router-link>
          <button @click.prevent="eliminar(producto.id as number)"><i class="pi pi-trash" style="font-size: 1.5rem"></i></button>
                  </td>     
       
       
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { onMounted, toRefs } from 'vue'
import useProductosStore from '@/stores/producto'
const { productos } = toRefs(useProductosStore())
const { getAll, destroy } = useProductosStore() 

onMounted(async () => {
  await getAll()
})
async function eliminar(id: number) {
  if (confirm('¿Estás seguro de eliminar esta producto ' + id + '?')) {
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

.pi-pencil
{
  cursor: pointer;
  color: #c4d11a;
}
.volver{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
}
</style>
