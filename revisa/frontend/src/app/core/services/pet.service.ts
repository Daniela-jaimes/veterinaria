import {
    Injectable,inject
} 
from '@angular/core'; 
import {
    ApiService
} 
from './api.service'; 
import {
    Pet
} 
from '../models/entities.models';
@Injectable({
    providedIn:'root'
}) 
export class PetService {
    private api=inject(ApiService); 
    list(page:number,limit:number,search=''){
        return this.api.list<Pet>('pets',page,limit,{search});
    } 
    create(p:Partial<Pet>){
        return this.api.create<Pet>('pets',p)
    } 
    update(id:number,p:Partial<Pet>){
        return this.api.update<Pet>('pets',id,p)
    } 
    remove(id:number){
        return this.api.remove('pets',id)
    } 
}
