import type { Talles} from "./Talles";
import type { Socios } from "./Socios";

export interface Compras{
id?: number;
descripcion: string;
precio: number;
cantidad: number;
talle?:Talles;
categoria?: string;
socio?:Socios;
estado?: string; // Nuevo campo para el estado de la compra
}
