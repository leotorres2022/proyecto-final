<template>
  <h1 class="titulo">Stock de Productos</h1>

  <div class="volver">
    <router-link :to="{ name: 'configuraciones' }">
      <i
        class="pi pi-arrow-circle-left"
        style="font-size: 2rem"
      ></i>
    </router-link>
  </div>

  <table>
    <thead>
      <tr>
        <th>Producto</th>
        <th>Categoría</th>
        <th>Talle</th>
        <th>Stock</th>
      </tr>
    </thead>

    <tbody>
      <tr
        v-for="item in stocks"
        :key="item.id"
      >
        <td>{{ item.producto_nombre }}</td>

        <td>{{ item.categoria_nombre }}</td>

        <td>{{ item.talle_nombre }}</td>

        <td>
          {{ item.stock }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">

import { onMounted, ref } from 'vue'
import UseProductosStore from '@/stores/producto'

const productosStore = UseProductosStore()

const stocks = ref<any[]>([])

onMounted(async () => {

  const data = await productosStore.getStockTodos()

  if (data) {
    stocks.value = data
  }

})

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
