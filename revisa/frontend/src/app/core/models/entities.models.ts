export interface Customer { 
    customer_id:number; 
    first_name:string; 
    last_name:string; 
    phone:string|null; 
    email:string|null; 
    address:string|null; 
    emergency_contact:string|null; 
    is_active:boolean; 
    created_at:string; }
export interface Pet { 
    pet_id:number; 
    customer_id:number; 
    breed_id:number; 
    name:string; 
    birth_date:string|null; 
    sex:'male'|'female'|'unknown'; 
    microchip_number:string|null; 
    is_neutered:boolean; 
    is_active:boolean; }
export interface Appointment { 
    appointment_id:number;
    pet_id:number; 
    vet_id:number; 
    scheduled_at:string; 
    reason:string; 
    status:'scheduled'|'in_consultation'|'completed'|'cancelled'|'no_show'; 
    notes?:string|null; 
}
