<template>
  <div class="flyer-container">
    <div class="flyer-card">
      
      <!-- Encabezado Estilo Graffiti/Pincel -->
      <header class="flyer-header">
        <h1 class="text-impact">¡JUGAMOS <br> <span class="blue-text">DE VISITANTE!</span></h1>
        <div class="contra-label">
          <span class="line"></span> CONTRA <span class="line"></span>
        </div>
      </header>

      <!-- Escudo y Nombre del Rival -->
      <section class="rival-section">
        <div class="rival-box">
          <h2 v-if="!isEditing" class="rival-name">{{ rival }}</h2>
          <input v-else v-model="rival" class="rival-input" placeholder="Nombre del rival" />
        </div>
      </section>

      <!-- Horarios con Estilo de Pincelada -->
      <section class="schedule-flyer">
        <div class="schedule-header">
          <h3 class="schedule-title">
            <i class="pi pi-clock"></i> HORARIOS DE LOS PARTIDOS
          </h3>
          <button @click="toggleEdit" class="btn-edit">
            <i class="pi" :class="isEditing ? 'pi-check' : 'pi-pencil'"></i>
            {{ isEditing ? 'Guardar' : 'Editar' }}
          </button>
        </div>
        
        <div class="match-list">
          <div class="match-row" v-for="(h, index) in horarios" :key="index">
            <input v-if="isEditing" v-model="h.cat" class="brush-bg cat-box edit-input" placeholder="Categoría" />
            <div v-else class="brush-bg cat-box">{{ h.cat }}</div>
            <div class="ball-icon">⚽</div>
            <input v-if="isEditing" v-model="h.time" class="brush-bg time-box edit-input" placeholder="Hora" />
            <div v-else class="brush-bg time-box">{{ h.time }}</div>
          </div>
        </div>
      </section>

     <footer class="flyer-footer">
        <!-- Botón para ver tablas -->
        <div class="actions-container">
          <router-link :to="{ name: 'division_list' }" class="btn-action">
            VER TABLAS Y RESULTADOS
            <i class="pi pi-arrow-right"></i>
          </router-link>
        </div>

        <p class="motto">¡VAMOS GUERREROS DEL SUR!</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import fondoUrl from '@/assets/fondo_futbol.jpg';

const isEditing = ref(false);
const rival = ref('DEPORTIVO PATAGONES');

const horarios = ref([
  { cat: '8va', time: '11:00 hs' },
  { cat: '7ma', time: '12:30 hs' },
  { cat: '6ta', time: '14:00 hs' },
  { cat: '5ta', time: '15:30 hs' },
  { cat: '4ta', time: '17:00 hs' }
]);

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
  if (!isEditing.value) {
    // Guardar en localStorage
    localStorage.setItem('horarios', JSON.stringify(horarios.value));
    localStorage.setItem('rival', rival.value);
  }
};

onMounted(() => {
  // Cargar desde localStorage
  const savedHorarios = localStorage.getItem('horarios');
  const savedRival = localStorage.getItem('rival');
  if (savedHorarios) {
    horarios.value = JSON.parse(savedHorarios);
  }
  if (savedRival) {
    rival.value = savedRival;
  }
});

const backgroundStyle = {
  backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.35)), url(${fondoUrl})`
};
</script>
<style scoped>
/* Importación de fuentes para el estilo deportivo/graffiti */
@import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Oswald:wght@500;700&display=swap');

/* 1. CONTENEDOR DE PANTALLA COMPLETA */
.flyer-container {
  width: 100vw;
  min-height: calc(100vh - 60px); /* Ajusta los 60px al alto de tu navbar */
  display: flex;
  justify-content: center;
  align-items: center;
  
  /* Imagen de fondo desde assets */
  background-image: url('@/assets/fondo_futbol.jpg'); 
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  
  /* Centrado forzado para evitar bordes blancos */
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  padding: 40px 20px;
  box-sizing: border-box;
}

/* 2. TARJETA PRINCIPAL (EL FLYER) */
.flyer-card {
  width: 95%;
  max-width: 900px; /* Tamaño grande para que no quede chiquito */
  background: rgba(255, 255, 255, 0.92); /* Efecto papel con transparencia */
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  font-family: 'Oswald', sans-serif;
  
  /* Sombra imponente solicitada */
  box-shadow: 
    0 10px 20px rgba(0, 0, 0, 0.1), 
    0 30px 60px rgba(0, 0, 0, 0.15), 
    0 60px 100px rgba(0, 0, 0, 0.2);
    
  border: 1px solid rgba(255, 255, 255, 0.4);
}

/* 3. CABECERA Y TÍTULOS */
.flyer-header {
  margin-bottom: 40px;
}

.text-impact {
  font-family: 'Permanent Marker', cursive;
  font-size: clamp(2.5rem, 7vw, 4.5rem); /* Tamaño dinámico y grande */
  line-height: 1;
  color: #1e293b;
  transform: rotate(-2deg); /* Efecto inclinado como la imagen */
  margin: 0;
}

.blue-text {
  color: #1976d2; /* Tu azul característico */
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

/* 4. SECCIÓN DEL RIVAL */
.rival-section {
  margin: 40px 0;
}

.rival-box {
  background: #001f3f; /* Azul muy oscuro profundo */
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  padding: 30px;
  border-radius: 12px;
  /* Efecto de recorte irregular de image_e9e6c2.jpg */
  clip-path: polygon(0% 0%, 100% 4%, 100% 100%, 0% 96%);
}

.escudo-rival {
  width: 100px;
  height: 100px;
  object-fit: contain;
  filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));
}

.rival-name {
  font-size: 2.2rem;
  font-weight: 700;
  text-align: left;
  line-height: 1.1;
  margin: 0;
}

/* 5. GRILLA DE HORARIOS ESTILO PINCELADA */
.schedule-flyer {
  margin-top: 50px;
}

.schedule-title {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
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
}

.brush-bg {
  background: #1976d2;
  color: black;
  padding: 12px 0;
  font-size: 1.8rem;
  width: 180px; /* Ancho para que todas las cajas midan igual */
  font-weight: 700;
  /* Simulación de trazo de pincel */
  clip-path: polygon(4% 0%, 100% 0%, 96% 100%, 0% 100%);
}

.ball-icon {
  font-size: 2rem;
  animation: rotateBall 10s linear infinite;
}

@keyframes rotateBall {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 6. BOTÓN Y FOOTER */
.flyer-footer {
  margin-top: 50px;
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
  box-shadow: 0 10px 20px rgba(25, 118, 210, 0.3);
}

.btn-action:hover {
  background: #1565c0;
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 15px 30px rgba(25, 118, 210, 0.4);
}

.motto {
  font-family: 'Permanent Marker', cursive;
  color: #94a3b8;
  font-size: 1.2rem;
  margin-top: 40px;
}

/* 7. RESPONSIVE (MÓVILES) */
@media (max-width: 600px) {
  .flyer-card { padding: 30px 15px; }
  .rival-box { flex-direction: column; text-align: center; gap: 15px; }
  .rival-name { text-align: center; font-size: 1.6rem; }
  .brush-bg { width: 120px; font-size: 1.3rem; }
  .text-impact { font-size: 2.2rem; }
}

/* Estilos para edición */
.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-edit {
  background: white;
  color: #1976d2;
  border: 2px solid #1976d2;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-edit:hover {
  background: #1976d2;
  color: white;
}

.edit-input {
  border: 2px solid #1976d2;
  border-radius: 5px;
  padding: 5px;
  text-align: center;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.9);
}

.edit-select {
  border: 2px solid #1976d2;
  border-radius: 5px;
  padding: 5px;
  text-align: center;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.9);
  width: 100%;
}

.division-select {
  margin-top: 20px;
  text-align: center;
}

.division-select label {
  color: white;
  font-weight: bold;
  margin-right: 10px;
}

.division-select select {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #1976d2;
  border-radius: 5px;
  padding: 5px;
  font-weight: bold;
}

.rival-input {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #1976d2;
  border-radius: 5px;
  padding: 10px;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  color: white;
  width: 100%;
}
</style>