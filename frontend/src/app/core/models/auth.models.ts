export interface User { 
    user_id:number; 
    username:string; 
    email:string; 
    role:'admin'|'veterinarian'|'receptionist'; 
    vet_id:number|null; 
    is_active:boolean; 
    last_login:string|null; 
    created_at:string; 
    vet?:unknown|null; }
export interface TokenResponse { 
    access_token:string; 
    token_type:string; 
    expires_in:number; 
    user:User; }
export interface Page<T> { 
    items:T[]; 
    total:number; 
    limit:number; 
    offset:number; }
