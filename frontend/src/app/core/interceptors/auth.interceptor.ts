import { HttpInterceptorFn } 
from '@angular/common/http';
import { inject } 
from '@angular/core'; 
import { Router } 
from '@angular/router'; 
import { catchError, throwError } 
from 'rxjs'; import { AuthService } 
from '../services/auth.service';
export const authInterceptor:HttpInterceptorFn=(req,next)=>{const auth=inject(AuthService),router=inject(Router),
    token=auth.token();const isLogin=req.url.endsWith('/auth/login');
    const request=token&&!isLogin?req.clone({setHeaders:{Authorization:`Bearer ${token}`}}):
    req;return next(request).pipe(catchError(err=>{if(err.status===401&&!isLogin)
        {auth.logout();router.navigate(['/login']);}return throwError(()=>err);}));};
