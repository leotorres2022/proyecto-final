<template>

  <div>
    <form @submit.prevent="crear">
      <div >
        <label for="" >Nombre de socio</label>
        <input type="text" name="create" v-model="socio.nombre">
        <label for="" >DNI</label>
        <input type="text" name="create" v-model="socio.dni" required>
 <label for="division">División</label>

<select v-model="socio.division" required>
  <option value="" disabled>Seleccionar división</option>
  <option   v-for="division in divisions"  :key="division.id"  :value="division.nombre"  >
    {{ division.nombre }}
  </option>
</select>
        <label for="" >telefono</label>
        <input type="text" name="create" v-model="socio.telefono">
        <label for="" >Direccion</label>
        <input type="text" name="create" v-model="socio.direccion">
        <label for="" >Email</label>
        <input type="email" name="create" v-model="socio.email">
      </div>
      <button type="submit">Crear Socio</button>
    </form>
    <div class="volver" >
          <router-link :to="{name:'home'}"><i class="pi pi-arrow-circle-left" style="font-size: 2rem"></i></router-link>
    </div>
  </div>
</template>
<script setup lang="ts">

import { onMounted } from 'vue'
import { toRefs,ref} from 'vue'
import  UseSociosStore from '../../stores/socios'
import  UseDivisionesStore from '../../stores/division'
const divisionesStore = UseDivisionesStore()
const { divisions} = toRefs(divisionesStore);
const {socio: socio} = toRefs(UseSociosStore())
const {create} = UseSociosStore()
const limpiarFormulario = () => {
  socio.value = {
    nombre: '',
    dni: '',
    division: '',
    telefono: '',
    direccion: '',
    email: '',
    estado: 'Pendiente'
  }
}
onMounted(async () => {
  limpiarFormulario()

  try {
    await divisionesStore.getAll();
  } catch (error) {
    console.error("Error al cargar las divisiones:", error);
  }

 
})
const crear = async ()=> {
  if (!socio.value.nombre)  {
    alert('El nombre del socio es obligatorio')
  }
  else if (!socio.value.telefono) {
    alert('El telefono del socio es obligatorio')
  }
  else if (!socio.value.dni) {
    alert('El DNI del socio es obligatorio')
  }
  else if (!socio.value.direccion) {
    alert('La direccion del socio es obligatoria')
  }
  else if (!socio.value.email) {
    alert('El email del socio es obligatorio')
  }
else {
    try {
      const response = await create(socio.value)
      limpiarFormulario()
      alert('Socio creado correctamente')
      console.log(response)
    } catch (error: any) {
      console.error('Error creando socio:', error)
      let mensaje = 'Error al crear el socio.'
      if (error && typeof error === 'object') {
        if (Array.isArray(error.email)) {
          mensaje = `Email inválido o ya registrado: ${error.email.join(' ')}`
        } else if (error.email) {
          mensaje = `Email inválido o ya registrado: ${error.email}`
        } else {
          mensaje = JSON.stringify(error)
        }
      }
      alert(mensaje)
    }
  }
}

</script>

<style scoped>
form {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 0.8rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.volver{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
}

</style>
