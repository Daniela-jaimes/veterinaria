import { Injectable, inject } from '@angular/core';

import { Pet } from '../models/entities.models';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class PetService {
  private api = inject(ApiService);
  private readonly resource = 'pets';

  list(page: number, limit: number, search = '', species = '') {
    return this.api.list<Pet>(this.resource, page, limit, { search, species });
  }

  create(payload: Partial<Pet>) {
    return this.api.create<Pet>(this.resource, payload);
  }

  update(id: number, payload: Partial<Pet>) {
    return this.api.update<Pet>(this.resource, id, payload);
  }

  remove(id: number) {
    return this.api.remove(this.resource, id);
  }
}
