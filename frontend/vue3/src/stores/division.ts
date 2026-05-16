import { defineStore } from "pinia"
import { ref } from "vue"
import ApiService from "@/services/ApiService"
import type { Torneos_division } from '@/interfaces/Torneos_division'

const useDivisionStore = defineStore('division', () => {
  // --- ESTADO ---
  const divisions = ref<Array<Torneos_division>>([])
  const division = ref<Torneos_division>({
    id: 0,
    nombre: ''      
  })
  
  // Nuevos estados para la tabla y los resultados
  const tablaPosiciones = ref<Array<any>>([])
  const partidos = ref<Array<any>>([])

  const url = 'api/torneos/division/'

  // --- ACCIONES ---

  // 1. Obtener todas las divisiones (para el select)
  async function getAll() {
    try {
      const data = await ApiService.getAll(url)
      divisions.value = data
    } catch (error) {
      console.error('Error al obtener divisiones:', error)
    }
  }

  // 2. Obtener la tabla de posiciones calculada por Django
async function getTabla(divisionId: number) {
  try {
    // Forzamos la ruta completa sin depender tanto de la variable 'url'
    const rutaFinal = `api/torneos/division/${divisionId}/tabla/`;
    console.log("Llamando a:", rutaFinal); // REVISA ESTO EN LA CONSOLA (F12)
    
    const data = await ApiService.getAll(rutaFinal);
    console.log("Respuesta de Tabla:", data);
    tablaPosiciones.value = data;
  } catch (error) {
    console.error("Error en getTabla:", error);
  }
}
 // 3. Obtener los partidos/resultados de la división (CON FILTRO DE FECHA)
async function getPartidos(divisionId: number, fecha: number | null = null) {
  try {
    // 1. Empezamos con la URL base
    let endpoint = `${url}${divisionId}/partidos/`;

    // 2. Si se pasó una fecha, agregamos el parámetro de consulta (Query Param)
    if (fecha !== null) {
      endpoint += `?fecha=${fecha}`;
    }

    // 3. Llamamos a la API con la URL final (ej: .../partidos/?fecha=3)
    const data = await ApiService.getAll(endpoint);
    partidos.value = data;
    
  } catch (error) {
    console.error('Error al obtener partidos:', error);
    // Es buena idea limpiar los partidos si hay error para no mostrar datos viejos
    partidos.value = [];
  }
}

  // --- CRUD BÁSICO ---
  async function create(division: Torneos_division) {
    const response = await ApiService.create(url, division)
    if (response) {
      await getAll() // Refrescar lista tras crear
      return response
    }
  }

  async function update(division: Torneos_division) {
    if (division.id) {
      const data = await ApiService.update(url, division.id, division)
      if (data) {
        await getAll() // Refrescar lista tras actualizar
        return data
      }
    }
  }

  async function destroy(id: number) {
    const data = await ApiService.destroy(url, id)
    if (data) {
      await getAll() // Refrescar lista tras borrar
      return data
    }
  }

  // --- RETORNO ---
  // IMPORTANTE: Debes incluir las nuevas variables y funciones aquí para que Vue las vea
  return { 
    divisions, 
    division, 
    tablaPosiciones, 
    partidos, 
    getAll, 
    getTabla, 
    getPartidos, 
    destroy, 
    create, 
    update 
  }
})

export default useDivisionStore