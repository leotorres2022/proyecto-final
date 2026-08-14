<template>
  <div class="detalle-socio">
    <h2><i class="pi pi-id-card" style="margin-right: 8px"></i>Detalle de la Compra</h2>
    <p><strong>Socio:</strong> <span class="dato">{{ typeof compra.socio === 'object' ? compra.socio?.nombre : (compra.socio || 'Sin nombre') }}</span></p>
    <p><strong>Total:</strong> <span class="dato">{{ compra.total ?? 0 }}</span></p>
    <p><strong>Fecha:</strong> <span class="dato">{{ formatoFecha(compra.fecha) }}</span></p>
    <p><strong>Estado:</strong> <span class="dato">{{ compra.estado || 'Sin estado' }}</span></p>
  </div>

  <div class="detalle-productos" v-if="compra.detalles?.length">
    <h3>Productos</h3>
    <table>
      <thead>
        <tr>
          <th>Producto</th>
          <th>Cantidad</th>
          <th>Precio unitario</th>
          <th>Subtotal</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(detalle, index) in compra.detalles" :key="detalle.id ?? (typeof detalle.producto_id === 'object' ? detalle.producto_id.id : detalle.producto_id) ?? index">
          <td>{{ typeof detalle.producto === 'object' ? detalle.producto?.nombre : 'Producto desconocido' }}</td>
          <td>{{ detalle.cantidad }}</td>
          <td>{{ detalle.precio_unitario }}</td>
          <td>{{ (Number(detalle.precio_unitario) * Number(detalle.cantidad)).toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div v-else class="detalle-productos empty-state">
    <p>No hay detalles de productos para esta compra.</p>
  </div>

  <div class="volver">
    <router-link :to="{ name: 'compras_list' }"><i class="pi pi-arrow-circle-left" style="font-size: 2rem"></i></router-link>
  </div>
</template>

<script setup lang="ts">
import { onMounted, toRefs } from 'vue'
import UseComprasStore from '../../stores/compras'
import { useRoute } from 'vue-router'

const route = useRoute()
const comprasStore = UseComprasStore()
const { compra, compras } = toRefs(comprasStore)
const { getAll } = comprasStore

const formatoFecha = (fecha: string | undefined) => {
  if (!fecha) return 'Sin fecha'
  return fecha.slice(0, 10)
}

onMounted(async () => {
  await getAll()
  const id = Number(route.params.id)
  const encontrada = compras.value.find(c => c.id === id)
  compra.value = encontrada ?? {
    id: 0,
    total: 0,
    fecha: undefined,
    estado: 'pendiente',
    socio: undefined,
    detalles: []
  }

  if (!encontrada) {
    console.error('Compra no encontrada')
  }
})
</script>

<style scoped>
.detalle-socio {
  max-width: 800px;
  margin: 2rem auto 1.5rem;
  padding: 2rem 2.5rem;
  background-color: #fdfdfd;
  border-radius: 18px;
  border: 1px solid rgba(0, 123, 255, 0.12);
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.08);
  color: #1f2937;
  font-family: 'Segoe UI', sans-serif;
}

.detalle-socio h2 {
  text-align: center;
  color: #0f172a;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.detalle-socio p {
  margin: 0.85rem 0;
  font-size: 1.05rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.detalle-socio p strong {
  color: #0f172a;
}

.dato {
  color: #2563eb;
  font-weight: 700;
}

.detalle-productos {
  max-width: 800px;
  margin: 0 auto 1.5rem;
  padding: 1.5rem 2rem;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  border-radius: 18px;
  border: 1px solid rgba(14, 165, 233, 0.12);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

.detalle-productos h3 {
  margin-bottom: 1rem;
  font-size: 1.4rem;
  color: #0f172a;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 100%;
}

th,
td {
  padding: 1rem 0.85rem;
  text-align: left;
}

thead th {
  color: #111827;
  font-weight: 700;
  border-bottom: 2px solid rgba(15, 23, 42, 0.12);
}

tbody tr {
  transition: background-color 0.2s ease;
}

tbody tr:nth-child(even) {
  background-color: rgba(15, 23, 42, 0.03);
}

tbody tr:hover {
  background-color: rgba(59, 130, 246, 0.08);
}

td {
  color: #334155;
  border-bottom: 1px solid rgba(148, 163, 184, 0.16);
}

.empty-state {
  text-align: center;
  color: #475569;
  font-size: 1rem;
}

.volver {
  display: flex;
  justify-content: center;
  margin: 2rem auto 3rem;
}

.volver a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: #2563eb;
  color: #ffffff;
  border-radius: 50%;
  text-decoration: none;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.volver a:hover {
  transform: translateY(-2px);
  background: #1d4ed8;
}
</style>
