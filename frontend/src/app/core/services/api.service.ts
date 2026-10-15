import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Page } from '../models/auth.models';

export type QueryFilters = Record<string, string | number | boolean | null | undefined>;

/**
 * Cliente CRUD genérico: único punto que habla con el backend para los recursos.
 */
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = environment.apiUrl;

  list<T>(resource: string, page = 1, limit = 10, filters: QueryFilters = {}): Observable<Page<T>> {
    let params = new HttpParams()
      .set('limit', limit)
      .set('offset', (page - 1) * limit);

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params = params.set(key, String(value));
      }
    });

    return this.http.get<Page<T>>(`${this.baseUrl}/${resource}`, { params });
  }

  get<T>(resource: string, id: number): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}/${resource}/${id}`);
  }

  create<T>(resource: string, payload: unknown): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}/${resource}`, payload);
  }

  update<T>(resource: string, id: number, payload: unknown): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}/${resource}/${id}`, payload);
  }

  remove(resource: string, id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${resource}/${id}`);
  }
}
