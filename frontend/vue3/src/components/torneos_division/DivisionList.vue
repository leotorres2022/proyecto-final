<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import useDivisionStore from "@/stores/division"; 

// Acceso al store de Pinia
const store = useDivisionStore();
const { divisions, tablaPosiciones, partidos } = storeToRefs(store);

// --- ESTADO LOCAL NUEVO ---
const divisionSeleccionada = ref<number | null>(null);
const fechaSeleccionada = ref<number | null>(3); //hasta la fecha 3 que es la que cargue en el backend
const cargando = ref(false);

onMounted(async () => {
  try {
    await store.getAll();
  } catch (error) {
    console.error("Error al cargar las divisiones:", error);
  }
});

// Función para cargar partidos 
const cargarPartidos = async () => {
  if (divisionSeleccionada.value) {
    // Pasamos el ID de división y la fecha seleccionada al store
    await store.getPartidos(divisionSeleccionada.value, fechaSeleccionada.value);
  }
};

// Observador para actualizar datos al cambiar la selección de DIVISIÓN
watch(divisionSeleccionada, async (nuevoId) => {
  if (nuevoId) {
    cargando.value = true;
    try {
      // Al cambiar de división, cargamos la tabla completa y los partidos de la fecha elegida
      await Promise.all([
        store.getTabla(nuevoId),
        cargarPartidos() 
      ]);
    } catch (error) {
      console.error("Error al cargar datos del servidor:", error);
    } finally {
      cargando.value = false;
    }
  }
});
</script>

<template>
  <div class="container-full">
    <header class="header-dashboard">
      <div class="header-content">
        <h1 class="titulo">Estadísticas y Resultados del Torneo</h1>
        <router-link :to="{ name: 'division_home' }" class="btn-back">
          <i class="pi pi-arrow-circle-left"></i>
          <span>Volver</span>
        </router-link>
      </div>
    </header>

    <div class="card selector-card">
      <div class="selector-content">
        <label for="division-select"><i class="pi pi-filter"></i> Filtrar por Categoría:</label>
        <select 
          id="division-select" 
          v-model="divisionSeleccionada" 
          class="custom-select"
        >
          <option :value="null" disabled>-- Seleccione una división para visualizar la información --</option>
          <option v-for="d in divisions" :key="d.id" :value="d.id">
            {{ d.nombre }}
          </option>
        </select>
        
      </div>
    </div>

    <div v-if="cargando" class="status-box">
      <i class="pi pi-spin pi-spinner" style="font-size: 3rem"></i>
      <p>Procesando estadísticas en tiempo real...</p>
    </div>

    <div v-else-if="divisionSeleccionada" class="dashboard-layout">
      
      <section class="card data-section">
        <h3 class="section-title"><i class="pi pi-chart-line"></i> Tabla de Posiciones</h3>
        <div class="scrollable-table">
          <table class="tabla-posiciones">
            <thead>
              <tr>
                <th>Pos</th>
                <th class="text-left">Equipo</th>
                <th>PJ</th>
                <th>PG</th>
                <th>PE</th>
                <th>PP</th>
                <th>GF</th>
                <th>GC</th>
                <th>DG</th>
                <th class="pts-col">PTS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in tablaPosiciones" :key="item.equipo">
                <td class="pos-cell">{{ index + 1 }}</td>
                <td class="text-left team-bold">{{ item.equipo }}</td>
                <td>{{ item.pj }}</td>
                <td>{{ item.pg }}</td>
                <td>{{ item.pe }}</td>
                <td>{{ item.pp }}</td>
                <td>{{ item.gf }}</td>
                <td>{{ item.gc }}</td>
                <td :class="item.dg >= 0 ? 'text-success' : 'text-danger'">
                  {{ item.dg > 0 ? '+' + item.dg : item.dg }}
                </td>
                <td class="pts-cell">{{ item.pts }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="card data-section">
  <div class="section-header">
    <h3 class="section-title"><i class="pi pi-calendar"></i> Últimos Resultados</h3>
    
    <div class="filter-container">
      <select v-model="fechaSeleccionada" @change="cargarPartidos" class="fecha-select">
        <option :value="null">Todas las Fechas</option>
        <option v-for="n in 3" :key="n" :value="n">Fecha {{ n }}</option>
      </select>
    </div>
  </div>

  <div v-if="partidos.length === 0" class="no-matches">
    <i class="pi pi-info-circle"></i> No hay partidos registrados para esta fecha.
  </div>
  
  <div v-for="p in partidos" :key="p.id" class="match-item">
    <div class="match-main">
      <span class="team local">{{ p.nombre_local }}</span>
      <div class="score-pill" :class="{ 'not-played': !p.jugado }">
        {{ p.jugado ? p.goles_local : '-' }} : {{ p.jugado ? p.goles_visitante : '-' }}
      </div>
      <span class="team visitante">{{ p.nombre_visitante }}</span>
    </div>
    <div class="match-date">Fecha {{ p.fecha }}</div>
  </div>
</section>

    </div>

    <div v-else class="status-box empty-state">
      <i class="pi pi-th-large" style="font-size: 4rem"></i>
      <p>Seleccione una división del menú para comenzar.</p>
    </div>
  </div>
</template>

<style scoped>
/* Contenedor Fluido al 95% */
.container-full {
  width: 95%;
  margin: 0 auto;
  padding: 20px 0;
  font-family: 'Inter', sans-serif;
}

/* Header */
.header-dashboard {
  background: linear-gradient(135deg, #1e293b 0%, #007BFF 100%);
  border-radius: 15px;
  padding: 25px 40px;
  color: white;
  margin-bottom: 25px;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.titulo { margin: 0; font-size: 1.8rem; font-weight: 700; }
.btn-back { 
  display: flex; align-items: center; gap: 10px; color: white; 
  text-decoration: none; font-weight: 500; transition: opacity 0.2s;
}
.btn-back:hover { opacity: 0.8; }

/* Selector */
.selector-card { margin-bottom: 25px; }
.selector-content { display: flex; align-items: center; gap: 20px; }
.custom-select {
  flex-grow: 1; padding: 12px; border-radius: 8px; 
  border: 1px solid #cbd5e1; font-size: 1rem; color: #1e293b;
}

/* Layout Dashboard */
.dashboard-layout {
  display: grid;
  grid-template-columns: 2fr 1fr; /* 66% Tabla, 33% Resultados */
  gap: 25px;
  align-items: start;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
}

.section-title {
  margin-top: 0; margin-bottom: 20px; font-size: 1.25rem;
  color: #007BFF; display: flex; align-items: center; gap: 10px;
  border-bottom: 2px solid #f1f5f9; padding-bottom: 15px;
}

/* Tabla de Posiciones */
.scrollable-table { overflow-x: auto; }
.tabla-posiciones { width: 100%; border-collapse: collapse; }
.tabla-posiciones th {
  padding: 15px 10px; background: #f8fafc; color: #64748b;
  font-size: 0.75rem; text-transform: uppercase; font-weight: 600;
}
.tabla-posiciones td { padding: 18px 10px; text-align: center; border-bottom: 1px solid #f1f5f9; }
.text-left { text-align: left !important; }
.team-bold { font-weight: 600; color: #0f172a; }
.pos-cell { color: #94a3b8; font-weight: 700; }
.pts-col { background: #f1f5f9; }
.pts-cell { font-weight: 800; color: #007BFF; font-size: 1.1rem; background: #eff6ff; }
.text-success { color: #16a34a; font-weight: 600; }
.text-danger { color: #dc2626; font-weight: 600; }

/* Fixture de Partidos */
.match-item {
  border-bottom: 1px solid #f1f5f9; padding: 15px 0;
}
.match-main { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.team { flex: 1; font-weight: 500; font-size: 0.9rem; }
.visitante { text-align: right; }
.score-pill {
  background: #1e293b; color: white; padding: 4px 14px;
  border-radius: 6px; font-weight: 700; margin: 0 15px; min-width: 50px; text-align: center;
}
.not-played { background: #e2e8f0; color: #94a3b8; }
.match-date { text-align: center; font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; }

/* Estados */
.status-box { text-align: center; padding: 80px; color: #64748b; }
.empty-state { background: white; border-radius: 12px; border: 2px dashed #e2e8f0; }

@media (max-width: 1200px) {
  .dashboard-layout { grid-template-columns: 1fr; }
  .container-full { width: 98%; }
}
</style>