import { Injectable, inject } from '@angular/core';

import { Customer } from '../models/entities.models';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  private api = inject(ApiService);
  private readonly resource = 'customers';

  list(page: number, limit: number, search = '') {
    return this.api.list<Customer>(this.resource, page, limit, { search });
  }

  create(payload: Partial<Customer>) {
    return this.api.create<Customer>(this.resource, payload);
  }

  update(id: number, payload: Partial<Customer>) {
    return this.api.update<Customer>(this.resource, id, payload);
  }

  remove(id: number) {
    return this.api.remove(this.resource, id);
  }
}
