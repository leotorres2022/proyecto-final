<template>
  <div class="form-container">
    <div class="fecha-selector">
      <label for="fecha-input">Seleccionar Fecha:</label>
      <select id="fecha-input" v-model.number="fechaActual" class="fecha-select">
        <option v-for="n in 10" :key="n" :value="n">Fecha {{ n }}</option>
      </select>
    </div>

    <form @submit.prevent="guardarTodosLosPartidos" class="fixture-form">
      <div class="fixture-container">
        <div v-for="(partido, index) in partidos" :key="index" class="fixture-row-with-delete">
          <div class="fixture-row">
            <div class="fixture-input-group">
              <select v-model="partido.equipo_local" class="equipo-select" required>
                <option value="" disabled>Equipo Local</option>
                <option
                  v-for="equipo in equiposFiltrados"
                  :key="equipo.id"
                  :value="equipo.id"
                  :disabled="equipo.id === partido.equipo_visitante"
                >
                  {{ equipo.nombre }}
                </option>
              </select>
            </div>

            <div class="fixture-score-inputs">
              <input
                type="number"
                v-model.number="partido.goles_local"
                min="0"
                class="goles-input"
                placeholder="0"
              />
              <span class="separator">:</span>
              <input
                type="number"
                v-model.number="partido.goles_visitante"
                min="0"
                class="goles-input"
                placeholder="0"
              />
            </div>

            <div class="fixture-input-group">
              <select v-model="partido.equipo_visitante" class="equipo-select" required>
                <option value="" disabled>Equipo Visitante</option>
                <option
                  v-for="equipo in equiposFiltrados"
                  :key="equipo.id"
                  :value="equipo.id"
                  :disabled="equipo.id === partido.equipo_local"
                >
                  {{ equipo.nombre }}
                </option>
              </select>
            </div>
          </div>
          <button
            type="button"
            @click="eliminarPartido(index)"
            class="btn-eliminar"
            :disabled="partidos.length === 1"
          >
            ✕
          </button>
        </div>

        <button type="button" @click="agregarPartido" class="btn-agregar-fila">
          + Agregar Partido
        </button>

        <div class="fixture-footer">
          <span class="fecha-badge">FECHA {{ fechaActual }} - {{ partidos.length }} Partido(s)</span>
          <button type="submit" class="btn-guardar" :disabled="enviando || partidos.length === 0">
            {{ enviando ? 'Guardando...' : 'Guardar Todo' }}
          </button>
        </div>
      </div>
    </form>

    <p v-if="mensajeExito" class="alert success">{{ mensajeExito }}</p>
    <p v-if="mensajeError" class="alert error">{{ mensajeError }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { instance as axios } from '@/plugins/axios';

interface Partido {
  division: number | string;
  equipo_local: number | string;
  equipo_visitante: number | string;
  goles_local: number;
  goles_visitante: number;
  fecha: number;
  jugado: boolean;
}

const props = defineProps<{
  divisionId?: number | null;
  fechaInicial?: number | null;
}>();

const emit = defineEmits<{
  (e: 'guardado'): void;
}>();

const divisiones = ref<any[]>([]);
const equipos = ref<any[]>([]);
const fechaActual = ref(1);

const equiposFiltrados = computed(() => {
  if (!props.divisionId) return equipos.value;
  return equipos.value.filter((equipo) => Number(equipo.division) === Number(props.divisionId));
});

const partidos = ref<Partido[]>([
  {
    division: '',
    equipo_local: '',
    equipo_visitante: '',
    goles_local: 0,
    goles_visitante: 0,
    fecha: 1,
    jugado: true,
  },
]);

const enviando = ref(false);
const mensajeExito = ref('');
const mensajeError = ref('');

watch(
  () => props.divisionId,
  (value) => {
    if (value != null) {
      partidos.value.forEach((p) => (p.division = value));
    }
  },
  { immediate: true }
);

watch(
  () => props.fechaInicial,
  (value) => {
    if (value != null) {
      fechaActual.value = value;
      partidos.value.forEach((p) => (p.fecha = value));
    }
  },
  { immediate: true }
);

watch(fechaActual, (newFecha) => {
  partidos.value.forEach((p) => (p.fecha = newFecha));
});

const crearPartidoVacio = (): Partido => ({
  division: partidos.value[0]?.division || '',
  equipo_local: '',
  equipo_visitante: '',
  goles_local: 0,
  goles_visitante: 0,
  fecha: fechaActual.value,
  jugado: true,
});

const agregarPartido = () => {
  partidos.value.push(crearPartidoVacio());
};

const eliminarPartido = (index: number) => {
  if (partidos.value.length > 1) {
    partidos.value.splice(index, 1);
  }
};

onMounted(async () => {
  try {
    const resDivisiones = await axios.get('/api/torneos/division/');
    const resEquipos = await axios.get('/api/torneos/equipos/');

    divisiones.value = Array.isArray(resDivisiones.data) ? resDivisiones.data : [];
    equipos.value = Array.isArray(resEquipos.data) ? resEquipos.data : [];
  } catch (error) {
    console.error('Error al cargar datos iniciales:', error);
    mensajeError.value = 'No se pudieron obtener las divisiones o los equipos desde el servidor.';
  }
});

const guardarTodosLosPartidos = async () => {
  // Validar que ningún partido tenga equipos iguales
  for (const partido of partidos.value) {
    if (partido.equipo_local === partido.equipo_visitante) {
      mensajeError.value = 'Un equipo no puede jugar contra sí mismo.';
      return;
    }
  }

  // Validar que todos los campos requeridos estén completos
  for (const partido of partidos.value) {
    if (!partido.equipo_local || !partido.equipo_visitante) {
      mensajeError.value = 'Por favor, completa todos los equipos antes de guardar.';
      return;
    }
  }

  enviando.value = true;
  mensajeExito.value = '';
  mensajeError.value = '';

  try {
    // Guardar todos los partidos
    const promesas = partidos.value.map((partido) =>
      axios.post('/api/torneos/partidos/', partido)
    );

    await Promise.all(promesas);

    mensajeExito.value = `¡${partidos.value.length} partido(s) cargado(s) exitosamente!`;
    
    // Resetear: una fila vacía con la misma división y fecha
    partidos.value = [crearPartidoVacio()];
    
    emit('guardado');
  } catch (error: any) {
    console.error('Error al guardar los partidos:', error);
    mensajeError.value = error.response?.data?.detail || 'Ocurrió un error al intentar guardar los partidos.';
  } finally {
    enviando.value = false;
  }
};
</script>

<style scoped>
.form-container {
  padding: 20px;
  background-color: #f9fafb;
  border-radius: 8px;
}

.fecha-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.fecha-selector label {
  font-weight: 600;
  font-size: 0.95rem;
  color: #1e293b;
}

.fecha-select {
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background-color: #ffffff;
  color: #1e293b;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
}

.fecha-select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.fixture-form {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.fixture-container {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.fixture-row-with-delete {
  display: flex;
  align-items: stretch;
  border-bottom: 1px solid #e2e8f0;
}

.fixture-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 12px;
  padding: 16px;
  flex: 1;
}

.fixture-input-group {
  display: flex;
}

.equipo-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background-color: #ffffff;
  color: #1e293b;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
}

.equipo-select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.fixture-score-inputs {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.goles-input {
  width: 50px;
  padding: 8px;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  background-color: #ffffff;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 700;
  text-align: center;
}

.goles-input:focus {
  outline: none;
  border-color: #007BFF;
}

.separator {
  font-weight: 700;
  color: #1e293b;
  font-size: 1.2rem;
}

.btn-eliminar {
  background-color: #fee2e2;
  color: #dc2626;
  border: none;
  padding: 10px 8px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-left: 1px solid #e2e8f0;
}

.btn-eliminar:hover:not(:disabled) {
  background-color: #fecaca;
}

.btn-eliminar:disabled {
  background-color: #f3f4f6;
  color: #d1d5db;
  cursor: not-allowed;
}

.btn-agregar-fila {
  width: 100%;
  background-color: #ecfdf5;
  color: #059669;
  border: 2px dashed #10b981;
  padding: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-agregar-fila:hover {
  background-color: #d1fae5;
}

.fixture-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background-color: #f8fafc;
}

.fecha-badge {
  font-size: 0.7rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.btn-guardar {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-guardar:hover:not(:disabled) {
  background-color: #005ecb;
}

.btn-guardar:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}


.alert {
  margin-top: 12px;
  padding: 12px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
}

.success {
  background-color: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid #10b981;
}

.error {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid #ef4444;
}

</style>