const API=import.meta.env.VITE_API_URL||"http://localhost:8000";
export type User={id:number;name:string;email:string;active:boolean};
export type Client={id:number;name:string;phone?:string;email?:string;notes?:string;active:boolean;created_at:string};
export type Service={id:number;name:string;description?:string;duration_minutes:number;price:string;active:boolean};
export type Professional={id:number;name:string;phone?:string;email?:string;notes?:string;active:boolean;services:Service[]};
export type BusinessHour={id?:number;weekday:number;start_time:string;end_time:string;active:boolean};
export type Block={id:number;professional_id?:number;date:string;start_time:string;end_time:string;reason:string};
export type Appointment={id:number;client_id:number;service_id:number;professional_id:number;date:string;start_time:string;end_time:string;status:string;price:string;notes?:string;client:Client;service:Service;professional:Professional};
export const token=()=>localStorage.getItem("agendapro_token");
export async function api<T>(path:string,options:RequestInit={}):Promise<T>{const headers=new Headers(options.headers);headers.set("Content-Type","application/json");const t=token();if(t)headers.set("Authorization",`Bearer ${t}`);const res=await fetch(`${API}${path}`,{...options,headers});if(res.status===204)return undefined as T;const data=await res.json().catch(()=>({detail:"Não foi possível concluir"}));if(!res.ok)throw new Error(data.detail||"Erro na operação");return data}
export const money=(v:string|number)=>new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"}).format(Number(v));
export const brdate=(v:string)=>v?new Date(v+"T12:00:00").toLocaleDateString("pt-BR"):"—";
