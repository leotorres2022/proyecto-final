export interface Socios{
  id?: number;
  nombre: string;
  dni: string;
  division: string;
  direccion: string;
  email: string;
  telefono: string;
  estado: 'Activo' | 'Moroso' | 'Pendiente';
}
