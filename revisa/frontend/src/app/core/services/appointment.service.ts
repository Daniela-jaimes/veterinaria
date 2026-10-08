import {
    Injectable,inject
} 
from '@angular/core'; 
import {
    ApiService
} 
from './api.service'; 
import {
    Appointment
} 
from '../models/entities.models';
@Injectable({
    providedIn:'root'
}) export class AppointmentService {
    private api=inject(ApiService); 
    list(page:number,limit:number){return this.api.list<Appointment>('appointments',page,limit);

    } 
    create(p:Partial<Appointment>){
        return this.api.create<Appointment>('appointments',p)
    } 
    update(id:number,p:Partial<Appointment>){
        return this.api.update<Appointment>('appointments',id,p)
    } 
    remove(id:number){
        return this.api.remove('appointments',id)
    } 
}
