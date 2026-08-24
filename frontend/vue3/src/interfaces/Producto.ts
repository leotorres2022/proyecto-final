export interface Producto {
  id: number;
  nombre: string;
  precio: number;
  categoria: number;
  imagen?: string | null;
}