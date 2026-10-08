import {
    Injectable,inject
} 
from '@angular/core'; 
import {
    HttpClient,HttpParams
} 
from '@angular/common/http';
 import {
    environment
} 
from '../../../environments/environment'; 
import {
    Page
} 
from '../models/auth.models';
 import {
    Observable
}
 from 'rxjs';
@Injectable({
    providedIn:'root'
}) 
export class ApiService 
{private http=inject(HttpClient);
     private base=environment.apiUrl; 
     list<T>(resource:string,page=1,limit=10,filters:Record<string,string|number|boolean|null|undefined>={}):
     Observable<Page<T>>{
        let p=new HttpParams().set('limit',limit).set('offset',(page-1)*limit);
        Object.entries(filters).forEach(([k,v])=>{if(v!==null&&v!==undefined&&v!=='')p=p.set(k,String(v));});
        return this.http.get<Page<T>>(`${this.base}/${resource}`,{params:p});
    } 
    get<T>(r:string,id:number){
        return this.http.get<T>(`${this.base}/${r}/${id}`)
    } 
    create<T>(r:string,p:unknown){
        return this.http.post<T>(`${this.base}/${r}`,p)
    } 
    update<T>(r:string,id:number,p:unknown){
        return this.http.put<T>(`${this.base}/${r}/${id}`,p)
    }
    remove(r:string,id:number){
        return this.http.delete<void>(`${this.base}/${r}/${id}`)
    } 
}

