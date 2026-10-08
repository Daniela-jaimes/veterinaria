import { 
    Injectable, inject 
} 
from '@angular/core'; 
import { 
    HttpClient, HttpParams 
} 
from '@angular/common/http';
import { 
    Observable, tap 
}
 from 'rxjs'; 
 import { 
    environment
} 
from '../../../environments/environment'; 
import { 
    TokenResponse, User 
} 
from '../models/auth.models';
@Injectable({
    providedIn:'root'
}) 
export class AuthService { 
    private http=inject(HttpClient); 
    private readonly key='vet_access_token'; 
    private readonly userKey='vet_user'; 
    login(username:string,password:string):Observable<TokenResponse>{
        const body=new HttpParams().set('username',username).set('password',password);
        return this.http.post<TokenResponse>(`${environment.apiUrl}/auth/login`,body.toString(),
        {headers:{'Content-Type':'application/x-www-form-urlencoded'

        }
    }
)
.pipe(tap(r=>{
    localStorage.setItem(this.key,r.access_token);
    localStorage.setItem(this.userKey,JSON.stringify(r.user))
}));
}
 me():Observable<User>{
    return this.http.get<User>(`${environment.apiUrl}/auth/me`).pipe(tap(u=>localStorage.setItem(this.userKey,JSON.stringify(u))));
} 
logout(){
    localStorage.removeItem(this.key);localStorage.removeItem(this.userKey);
} 
token(){
    return localStorage.getItem(this.key)
}
 user():User|null{const raw=localStorage.getItem(this.userKey);
    return raw?JSON.parse(raw) as User:null
} 
isLoggedIn(){
    return !!this.token()
} 
}
