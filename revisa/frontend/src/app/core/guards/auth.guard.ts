import {CanActivateFn,Router} 
from '@angular/router'; 
import {inject} 
from '@angular/core'; 
import {AuthService} 
from '../services/auth.service';
export const authGuard:CanActivateFn=()=>{const a=inject(AuthService);return a.isLoggedIn()||inject(Router).createUrlTree(['/login']);};
export const adminGuard:CanActivateFn=()=>{const a=inject(AuthService);return a.user()?.role==='admin'||inject(Router).createUrlTree(['/']);};
