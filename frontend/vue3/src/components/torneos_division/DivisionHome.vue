<template>
  <div class="flyer-container" :style="backgroundStyle">
    <div class="flyer-card">
      <header class="flyer-header">
        <h1 class="text-impact">
          ¡JUGAMOS <br>
          <span class="blue-text">
            <section class="localia-section">
              <div class="localia-box">
                <h2 v-if="!isEditing" class="localia-name">
                  {{ condicion === 'local'
                    ? 'DE LOCAL'
                    : 'DE VISITANTE'
                  }}
                </h2>
                <select v-else v-model="condicion" class="rival-input">
                  <option value="local">
                    DE LOCAL
                  </option>
                  <option value="visitante">
                    DE VISITANTE
                  </option>
                </select>
              </div>
            </section>
          </span>
        </h1>
        <div class="contra-label">
          <span class="line"></span>
          CONTRA
          <span class="line"></span>
        </div>
      </header>
      <section class="rival-section">
        <div class="rival-box">
          <h2 v-if="!isEditing" class="rival-name">
            {{ rival }}
          </h2>
          <!-- EDICIÓN -->
          <input v-else v-model="rival" class="rival-input" placeholder="Nombre del rival" />
        </div>
      </section>
      <section class="schedule-flyer">
        <div class="schedule-header">
          <h3 class="schedule-title">
            <i class="pi pi-clock"></i>
            HORARIOS DE LOS PARTIDOS
          </h3>
          <button v-if="esAdmin" @click="toggleEdit" class="btn-edit">
            <i class="pi" :class="isEditing
              ? 'pi-check'
              : 'pi-pencil'"></i>
            {{ isEditing ? 'Guardar' : 'Editar' }}
          </button>
        </div>
        <div v-if="isEditing" class="match-list">
          <div class="match-row" v-for="(h, index) in horarios" :key="index">
            <!-- HORA -->
            <input v-model="h.time" class="brush-bg time-box edit-input" placeholder="Hora" />
            <select v-model="h.division" class="division-select" required>
              <option value="" disabled>
                Seleccionar división
              </option>
              <option v-for="division in divisions" :key="division.id" :value="division.nombre" :disabled="divisionYaElegida(
                division.nombre,
                index
              )
                ">
                {{ division.nombre }}
              </option>
            </select>
            <div class="ball-icon">
              ⚽
            </div>
          </div>
        </div>
        <div v-else class="schedule-table">
          <div class="table-header">
            <div>
              DIVISIÓN
            </div>
            <div>
              HORARIO
            </div>
          </div>
          <div v-for="(h, index) in horarios" :key="index" class="table-row">
            <div class="division-name">
              {{ h.division || 'Sin división' }}
            </div>
            <div class="table-time">
              {{ h.time }}
            </div>
          </div>
        </div>
      </section>
      <footer class="flyer-footer">
        <div class="actions-container">
          <router-link :to="{ name: 'division_list' }" class="btn-action">
            VER TABLAS Y RESULTADOS
            <i class="pi pi-arrow-right"></i>
          </router-link>
        </div>
        <p class="motto">
          ¡VAMOS GUERREROS DEL SUR!
        </p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
  toRefs
} from 'vue';
import fondoUrl from '@/assets/fondo_futbol.jpg';
import { useAuthStore } from '@/stores/auth';
import UseDivisionesStore
  from '../../stores/division';
const divisionesStore =
  UseDivisionesStore();
const { divisions } =
  toRefs(divisionesStore);
const userAuthStore =
  useAuthStore();
const isEditing = ref(false);
const rival = ref(
  'DEPORTIVO PATAGONES'
);
const condicion = ref('local');
const horarios = ref([
  {time: '11:00 hs',
    division: ''  },
  {time: '12:30 hs',
    division: ''  },
  {time: '14:00 hs',
    division: ''  },
  {time: '15:30 hs',
    division: '' }
]);
const esAdmin = computed(() => {
  return (
    userAuthStore.isAuthenticated &&
    userAuthStore.user?.groups?.includes('admin')
  );
});
const toggleEdit = () => {
  if (!esAdmin.value) {
    return;
  }
  isEditing.value = !isEditing.value;
  if (!isEditing.value) {
    localStorage.setItem(
      'horarios',
      JSON.stringify(horarios.value)
    );
    localStorage.setItem(
      'rival',
      rival.value
    );
    localStorage.setItem(
      'condicion',
      condicion.value
    );
  }
};
function divisionYaElegida(
  divisionNombre,
  indexActual
) {
  return horarios.value.some(
    (h, index) =>
      index !== indexActual &&
      h.division === divisionNombre
  );
}
onMounted(async () => {
  try {
    await divisionesStore.getAll();
  } catch (error) {
    console.error(
      'Error al cargar las divisiones:',
      error
    );
  }
  const savedHorarios =
    localStorage.getItem('horarios');
  if (savedHorarios) {
    try {
      horarios.value =
        JSON.parse(savedHorarios);
    } catch (error) {
      console.error(
        'Error al cargar horarios:',
        error
      );
    }
  }
  /* RIVAL */
  const savedRival =
    localStorage.getItem('rival');
  if (savedRival) {
    rival.value =
      savedRival;
  }
  const savedCondicion =
    localStorage.getItem('condicion');
  if (savedCondicion) {
    condicion.value =
      savedCondicion;
  }
});
const backgroundStyle = {
  backgroundImage:
    `linear-gradient(
      rgba(0, 0, 0, 0.35),
      rgba(0, 0, 0, 0.35)
    ),
    url(${fondoUrl})`
};
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Oswald:wght@500;700&display=swap');
.flyer-container {
  width: 100vw;
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url('@/assets/fondo_futbol.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  padding: 40px 20px;
  box-sizing: border-box;
}
.flyer-card {
  width: 95%;
  max-width: 900px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  font-family: 'Oswald', sans-serif;
  box-shadow:
    0 10px 20px rgba(0, 0, 0, 0.1),
    0 30px 60px rgba(0, 0, 0, 0.15),
    0 60px 100px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
}
.flyer-header {
  margin-bottom: 40px;
}
.text-impact {
  font-family: 'Permanent Marker', cursive;
  font-size: clamp(2.5rem, 7vw, 2.5rem);
  line-height: 1;
  color: #1e293b;
  transform: rotate(-2deg);
  margin: 0;
}
.blue-text {
  color: #1976d2;
  display: block;
}
.contra-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 3px;
}
.line {
  height: 2px;
  width: 50px;
  background: #cbd5e1;
}
.localia-section {
  display: flex;
  justify-content: center;
}
.localia-box {
  display: flex;
  justify-content: center;
  align-items: center;
}
.localia-name {
  margin: 0;
  font-family: 'Permanent Marker', cursive;
  font-size: 2.3rem;
  color: #1976d2;
  transform: rotate(-2deg);
}
.rival-section {
  margin: 40px 0;
}
.rival-box {
  background: #001f3f;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  padding: 30px;
  border-radius: 12px;
  clip-path: polygon(0% 0%,
      100% 4%,
      100% 100%,
      0% 96%);
}
.rival-name {
  font-size: 2.2rem;
  font-weight: 700;
  text-align: left;
  line-height: 1.1;
  margin: 0;
}
.rival-input {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #1976d2;
  border-radius: 5px;
  padding: 10px;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  color: #001f3f;
  width: 100%;
  box-sizing: border-box;
}
.rival-box .rival-input {
  width: 80%;
}
.schedule-flyer {
  margin-top: 50px;
}
.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.schedule-title {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.btn-edit {
  background: white;
  color: #1976d2;
  border: 2px solid #1976d2;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  font-family: 'Oswald', sans-serif;
  transition: all 0.3s;
}
.btn-edit:hover {
  background: #1976d2;
  color: white;
  transform: translateY(-2px);
}
.schedule-table {
  width: 100%;
  margin-top: 10px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow:
    0 8px 20px rgba(0, 0, 0, 0.12);
}
.table-header {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  background: #001f3f;
  color: white;
  padding: 15px 20px;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
}
.table-header div {
  text-align: center;
}
.table-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  align-items: center;
  min-height: 65px;
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}
.table-row:last-child {
  border-bottom: none;
}
.table-row:hover {
  background: #f8fafc;
}
.division-name {
  text-align: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: #001f3f;
}
.table-time {
  text-align: center;
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
  background: #1976d2;
  margin: 8px 15px;
  padding: 8px 15px;
  clip-path: polygon(4% 0%,
      100% 0%,
      96% 100%,
      0% 100%);
}
.match-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.match-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 10px;
  flex-wrap: wrap;
}
.brush-bg {
  background: #1976d2;
  color: black;
  padding: 12px 0;
  font-size: 1.8rem;
  width: 180px;
  font-weight: 700;
  clip-path: polygon(4% 0%,
      100% 0%,
      96% 100%,
      0% 100%);
}
.time-box {
  text-align: center;
}
.edit-input {
  border: 2px solid #1976d2;
  border-radius: 5px;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.9);
  color: #001f3f;
  font-family: 'Oswald', sans-serif;
  box-sizing: border-box;
}
.edit-input:focus {
  outline: none;
  box-shadow:
    0 0 0 3px rgba(25, 118, 210, 0.2);
}
.division-select {
  border: 2px solid #1976d2;
  border-radius: 5px;
  padding: 10px 15px;
  text-align: center;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.95);
  color: #001f3f;
  font-family: 'Oswald', sans-serif;
  font-size: 1rem;
  min-width: 180px;
  cursor: pointer;
  box-sizing: border-box;
}
.division-select:focus {
  outline: none;
  box-shadow:
    0 0 0 3px rgba(25, 118, 210, 0.2);
}
.division-select option:disabled {
  color: #999;
}
.ball-icon {
  font-size: 2rem;
  animation:
    rotateBall 10s linear infinite;
}
@keyframes rotateBall {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.flyer-footer {
  margin-top: 50px;
}
.actions-container {
  display: flex;
  justify-content: center;
}
.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 15px;
  background: #1976d2;
  color: white;
  padding: 20px 50px;
  font-size: 1.3rem;
  font-weight: 700;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow:
    0 10px 20px rgba(25, 118, 210, 0.3);
}
.btn-action:hover {
  background: #1565c0;
  transform:
    translateY(-3px) scale(1.02);
  box-shadow:
    0 15px 30px rgba(25, 118, 210, 0.4);
}

.motto {
  font-family: 'Permanent Marker', cursive;
  color: #94a3b8;
  font-size: 1.2rem;
  margin-top: 40px;
}
/*responsivo*/
@media (max-width: 600px) {
  .flyer-container {
    padding: 25px 10px;
  }
  .flyer-card {
    padding: 30px 15px;
  }
  .rival-box {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  .rival-name {
    text-align: center;
    font-size: 1.6rem;
  }
  .rival-box .rival-input {
    width: 95%;
  }
  .text-impact {
    font-size: 2.2rem;
  }
  .localia-name {
    font-size: 1.8rem;
  }
  .schedule-header {
    flex-direction: column;
    gap: 15px;
  }
  .schedule-title {
    font-size: 1.2rem;
  }
  .btn-edit {
    width: 100%;
  }
  /* TABLA */
  .table-header {
    font-size: 0.85rem;
    padding: 12px 5px;
  }
  .table-row {
    min-height: 55px;
  }
  .division-name {
    font-size: 1rem;
  }
  .table-time {
    font-size: 1.1rem;
    margin: 6px;
    padding: 7px 5px;
  }
  /* EDICIÓN */
  .match-row {
    flex-direction: column;
    gap: 12px;
  }
  .brush-bg {
    width: 140px;
    font-size: 1.3rem;
  }
  .division-select {
    width: 100%;
    min-width: 0;
  }
  .ball-icon {
    font-size: 1.8rem;
  }
  .btn-action {
    width: 100%;
    justify-content: center;
    padding: 15px 10px;
    font-size: 1rem;
  }
}
</style>