export interface Customer {
  customer_id: number;
  first_name: string;
  last_name: string;
  phone: string | null;
  email: string | null;
  address: string | null;
  emergency_contact: string | null;
  is_active: boolean;
  created_at: string;
}

export type PetSex = 'male' | 'female' | 'unknown';

export interface Pet {
  pet_id: number;
  customer_id: number;
  breed_id: number;
  name: string;
  birth_date: string | null;
  sex: PetSex;
  microchip_number: string | null;
  photo_url?: string | null;
  is_neutered: boolean;
  is_active: boolean;
}

export interface Breed {
  breed_id: number;
  species: string;
  name: string;
}

export interface Appointment {
  appointment_id: number;
  pet_id: number;
  vet_id: number;
  scheduled_at: string;
  reason: string;
  status: 'scheduled' | 'in_consultation' | 'completed' | 'cancelled' | 'no_show';
  notes?: string | null;
}
