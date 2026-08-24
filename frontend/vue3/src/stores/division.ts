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
  

  const tablaPosiciones = ref<Array<any>>([])
  const partidos = ref<Array<any>>([])

  const url = 'api/torneos/division/'

  async function getAll() {
    try {
      const data = await ApiService.getAll(url)
      divisions.value = data
    } catch (error) {
      console.error('Error al obtener divisiones:', error)
    }
  }

async function getTabla(divisionId: number) {
  try {
   
    const rutaFinal = `api/torneos/division/${divisionId}/tabla/`;
    console.log("Llamando a:", rutaFinal);
    const data = await ApiService.getAll(rutaFinal);
    console.log("Respuesta de Tabla:", data);
    tablaPosiciones.value = data;
  } catch (error) {
    console.error("Error en getTabla:", error);
  }
}

async function getPartidos(divisionId: number, fecha: number | null = null) {
  try {
   
    let endpoint = `${url}${divisionId}/partidos/`;

     if (fecha !== null) {
      endpoint += `?fecha=${fecha}`;
    }

   const data = await ApiService.getAll(endpoint);
    partidos.value = data;
    
  } catch (error) {
    console.error('Error al obtener partidos:', error);
    partidos.value = [];  /*limpio los partidos viejos si hay error para no mostrar viejos*/
  }
}
async function borrarPartidosFecha( divisionId: number, fecha: number | null = null) {
  try {
    const endpoint = `${url}${divisionId}/partidos/?fecha=${fecha}`
    const data = await ApiService.destroyUrl(endpoint)
    await getPartidos(divisionId, fecha)
    return data
  } catch (error) {
    console.error('Error al borrar los partidos:', error)
    throw error
  }
}


  async function create(division: Torneos_division) {
    const response = await ApiService.create(url, division)
    if (response) {
      await getAll() // Refresco la lista tras crear
      return response
    }
  }

  async function update(division: Torneos_division) {
    if (division.id) {
      const data = await ApiService.update(url, division.id, division)
      if (data) {
        await getAll() // Refresco la lista tras actualizar
        return data
      }
    }
  }

  async function destroy(id: number) {
    const data = await ApiService.destroy(url, id)
    if (data) {
      await getAll() // Refresco la lista tras borrar
      return data
    }
  }



  
  return { 
    divisions, 
    division, 
    tablaPosiciones, 
    partidos, 
    borrarPartidosFecha,  
    getAll, 
    getTabla, 
    getPartidos, 
    destroy, 
    create,
    update 
  }
})

export default useDivisionStore