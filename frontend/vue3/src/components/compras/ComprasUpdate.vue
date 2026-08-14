<template>
  <div>
    <h2>Actualizar Estado de Compra</h2>
    <form @submit.prevent="editar">
      <div class="detalle-socio">
        <label>Estado</label>
        <select v-model="compra.estado" class="dato" required>
          <option value="pendiente">Pendiente</option>
          <option value="finalizada">Finalizada</option>
          <option value="cancelada">Cancelada</option>
        </select>
      </div>
      <button type="submit" class="modificar">Actualizar estado</button>
    </form>
  </div>
  <div class="volver">
    <router-link :to="{name:'compras_list'}"><i class="pi pi-arrow-circle-left" style="font-size: 2rem"></i></router-link>
  </div>
</template>

<script setup lang="ts">
import { toRefs, onMounted } from 'vue';
import UseComprasStore from '../../stores/compras'
import { useRoute } from 'vue-router';

const route = useRoute()
const comprasStore = UseComprasStore()
const { compra, compras } = toRefs(comprasStore)
const { update } = comprasStore

onMounted(() => {
  const id = Number(route.params.id)
  const encontrada = compras.value.find(item => item.id === id)
  compra.value = encontrada ?? { id: 0, estado: 'pendiente' }
})

const editar = async () => {
  if (!compra.value.id) {
    alert('No se encontró la compra a modificar')
    return
  }

  try {
    await update({ id: compra.value.id, estado: compra.value.estado })
    alert('Estado actualizado correctamente')
  } catch (error) {
    console.error('Error al actualizar estado de compra:', error)
    alert('Error al actualizar estado. Revisa la consola para más detalles.')
  }
}
</script>

<style scoped>
.detalle-socio {
  max-width: 850px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  color: #333;
  font-family: 'Segoe UI', sans-serif;
  font-size: 1.3rem;
}

.detalle-socio h2 {
  text-align: center;
  color: #444;
  margin-bottom: 1.5rem;
}

.detalle-socio p {
  margin: 1rem 0;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
}

.dato {
  margin-left: 8px;
  color: #007BFF;
  font-weight: bold;
  font-size: 1.3rem;
}
.modificar {
  display: block;
  width: 10%;
  padding: 0.6rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.3rem;
  margin: 1rem auto;
  text-align: center;
}
.volver{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
}

</style>

