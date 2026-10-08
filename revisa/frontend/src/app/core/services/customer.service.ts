import {
    Injectable,inject
} 
from '@angular/core'; 
import {
    ApiService
} 
from './api.service'; 
import {
    Customer
}
from '../models/entities.models';
@Injectable({
    providedIn:'root'
}) 
export class CustomerService {
    private api=inject(ApiService);
    list(page:number,limit:number,search='')
    {
    return this.api.list<Customer>('customers',page,limit,{search});
    } 
    create(p:Partial<Customer>){
        return this.api.create<Customer>('customers',p)
    } 
    update(id:number,p:Partial<Customer>){
        return this.api.update<Customer>('customers',id,p)
    }
    remove(id:number){
        return this.api.remove('customers',id)} 
    }
