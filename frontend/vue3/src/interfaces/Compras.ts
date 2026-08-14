import type { Talles } from "./Talles";
import type { Socios } from "./Socios";
import type { Categorias } from "./Categorias";
import type { Producto } from "./Producto";

export interface DetalleCompra {
  id?: number;
  producto?: Producto | number;
  producto_id: Producto | number;
  cantidad: number;
  precio_unitario: number;
}

export interface Compras {
  id?: number;
  descripcion?: string;
  precio?: number;
  cantidad?: number;
  talle?: Talles | number;
  categoria?: Categorias | number;
  socio?: Socios | number;
  producto?: Producto | number;
  total?: number;
  fecha?: string;
  estado?: string;
  detalles?: DetalleCompra[];
}
