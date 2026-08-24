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

        <button  v-if="userAuthStore.isAuthenticated && (userAuthStore.user?.groups?.includes('admin'))"   type="button" class="btn-cargar-partido" @click="abrirFormularioCarga">
          <i class="pi pi-plus"></i>
          <span>{{ mostrarFormularioCarga ? 'Actualizar' : 'Cargar Partido' }}</span>
        </button>
      </div>
    </div>

    <div v-if="mostrarFormularioCarga" class="card formulario-card">
      <CargarPartido
        :division-id="divisionSeleccionada"
        :fecha-inicial="fechaSeleccionada"
        @guardado="handleGuardadoPartido"
      />
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
                <td class="text-left team-bold">
                  <span class="team-cell">
                    <img
                      v-if="item.escudo"
                      :src="item.escudo"
                      :alt="item.equipo"
                      class="team-logo"
                      @error="($event.target as HTMLImageElement).style.display = 'none'"
                    />
                    <span v-else class="team-logo-placeholder">⚽</span>
                    <span>{{ item.equipo }}</span>
                  </span>
                </td>
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
        <option v-for="n in 13" :key="n" :value="n">Fecha {{ n }}</option>
      </select>
       <button   type="button"   @click="borrarFecha"  :disabled="!fechaSeleccionada"  >  
      <i class="pi pi-trash"></i> Borrar Fecha {{ fechaSeleccionada }}
    </button>
    </div>
    
  </div>

  <div v-if="partidos.length === 0" class="no-matches">
    <i class="pi pi-info-circle"></i> No hay partidos registrados para esta fecha.
  </div>
  
  <div v-for="p in partidos" :key="p.id" class="match-item">
    <div class="fixture-row">
      <div class="fixture-team">{{ p.nombre_local }}</div>
      <div class="fixture-score" :class="{ 'not-played': !p.jugado }">
        {{ p.jugado ? p.goles_local : '-' }} : {{ p.jugado ? p.goles_visitante : '-' }}
      </div>
      <div class="fixture-team fixture-team-right">{{ p.nombre_visitante }}</div>
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
<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import useDivisionStore from "@/stores/division"; 
import CargarPartido from '@/components/torneos_division/CargarPartido.vue';
const store = useDivisionStore();
const { divisions, tablaPosiciones, partidos } = storeToRefs(store);
import { useAuthStore } from '@/stores/auth';
const userAuthStore = useAuthStore();

const divisionSeleccionada = ref<number | null>(null);
const fechaSeleccionada = ref<number | null>(3); 
const cargando = ref(false);
const mostrarFormularioCarga = ref(false);





onMounted(async () => {
  try {
    await store.getAll();
  } catch (error) {
    console.error("Error al cargar las divisiones:", error);
  }
});


const cargarPartidos = async () => {
  if (divisionSeleccionada.value) {
    cargando.value = true;
    try {
      await store.getPartidos(divisionSeleccionada.value, fechaSeleccionada.value);
    } finally {
      cargando.value = false;
    }
  }
};


async function borrarFecha() {
  if (    divisionSeleccionada.value === null ||    fechaSeleccionada.value === null  ) {
    alert('Seleccioná una división y una fecha')
    return
  }
  const confirmar = confirm(
    `¿Seguro que querés borrar todos los partidos de la Fecha ${fechaSeleccionada.value}?`
  )
  if (!confirmar) {
    return
  }
  try {
    await store.borrarPartidosFecha(   divisionSeleccionada.value,  fechaSeleccionada.value    )
    alert('Partidos de la fecha eliminados correctamente')
  } catch (error) {
    console.error('Error al borrar la fecha:', error)
    alert('No se pudo eliminar la fecha')
  }
}

const abrirFormularioCarga = async () => {
  if (!divisionSeleccionada.value) {
    return;
  }

  const siguienteFecha = (fechaSeleccionada.value ?? 0) + 1;
  fechaSeleccionada.value = siguienteFecha;
  mostrarFormularioCarga.value = true;
  await cargarPartidos();
};

const handleGuardadoPartido = async () => {
  mostrarFormularioCarga.value = false;
  if (divisionSeleccionada.value) {
    await cargarPartidos();
    await store.getTabla(divisionSeleccionada.value);
  }
};


watch(divisionSeleccionada, async (nuevoId) => {
  if (nuevoId) {
    cargando.value = true;
    try {

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
.selector-content { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }
.custom-select {
  flex-grow: 1; padding: 12px; border-radius: 8px; 
  border: 1px solid #cbd5e1; font-size: 1rem; color: #1e293b;
}
.btn-cargar-partido {
  display: inline-flex; align-items: center; gap: 8px;
  background: #007BFF; color: white; border: none; border-radius: 8px;
  padding: 12px 16px; font-weight: 600; cursor: pointer;
  transition: background 0.2s ease;
}
.btn-cargar-partido:hover { background: #005ecb; }
.btn-secondary {
  background: #475569;
}
.btn-secondary:hover { background: #334155; }
.formulario-card { margin-bottom: 25px; }

/*  Dashboard */
.dashboard-layout {
  display: grid;
  grid-template-columns: 2fr 1fr; /* 2/3 tabla  Tabla, 173 resultados Resultados */
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
.team-cell {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 28px;
}
.team-logo {
  width: 26px;
  height: 26px;
  object-fit: contain;
  flex-shrink: 0;
  display: block;
}
.team-logo-placeholder {
  width: 26px;
  height: 26px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #e2e8f0;
  color: #64748b;
  font-size: 0.9rem;
  flex-shrink: 0;
}
.pos-cell { color: #94a3b8; font-weight: 700; }
.pts-col { background: #f1f5f9; }
.pts-cell { font-weight: 800; color: #007BFF; font-size: 1.1rem; background: #eff6ff; }
.text-success { color: #16a34a; font-weight: 600; }
.text-danger { color: #dc2626; font-weight: 600; }

/* Fixture de Partidos */
.match-item {
  border-bottom: 1px solid #f1f5f9; padding: 12px 0;
}
.fixture-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 10px;
}
.fixture-team {
  font-weight: 600;
  font-size: 0.95rem;
  color: #0f172a;
}
.fixture-team-right {
  text-align: right;
}
.fixture-score {
  background: #1e293b; color: white; padding: 4px 12px;
  border-radius: 999px; font-weight: 700; min-width: 64px; text-align: center;
  justify-self: center;
}
.not-played { background: #e2e8f0; color: #94a3b8; }
.match-date {
  text-align: center;
  font-size: 0.72rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-top: 4px;
}

/* Estados */
.status-box { text-align: center; padding: 80px; color: #64748b; }
.empty-state { background: white; border-radius: 12px; border: 2px dashed #e2e8f0; }

@media (max-width: 1200px) {
  .dashboard-layout { grid-template-columns: 1fr; }
  .container-full { width: 98%; }
}
</style>