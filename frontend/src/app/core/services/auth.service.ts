import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { environment } from '../../../environments/environment';
import { TokenResponse, User } from '../models/auth.models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);

  private readonly tokenKey = 'vet_access_token';
  private readonly userKey = 'vet_user';

  login(username: string, password: string): Observable<TokenResponse> {
    // FastAPI (OAuth2PasswordRequestForm) espera un formulario, no JSON
    const body = new HttpParams()
      .set('username', username)
      .set('password', password);

    return this.http
      .post<TokenResponse>(`${environment.apiUrl}/auth/login`, body.toString(), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      .pipe(
        tap(response => {
          localStorage.setItem(this.tokenKey, response.access_token);
          localStorage.setItem(this.userKey, JSON.stringify(response.user));
        })
      );
  }

  me(): Observable<User> {
    return this.http
      .get<User>(`${environment.apiUrl}/auth/me`)
      .pipe(tap(user => localStorage.setItem(this.userKey, JSON.stringify(user))));
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
  }

  token(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  user(): User | null {
    const raw = localStorage.getItem(this.userKey);
    if (!raw) {
      return null;
    }
    try {
      return JSON.parse(raw) as User;
    } catch {
      return null;
    }
  }

  isLoggedIn(): boolean {
    return !!this.token();
  }
}
