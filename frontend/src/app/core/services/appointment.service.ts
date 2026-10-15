import { Injectable, inject } from '@angular/core';

import { Appointment } from '../models/entities.models';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class AppointmentService {
  private api = inject(ApiService);
  private readonly resource = 'appointments';

  list(page: number, limit: number) {
    return this.api.list<Appointment>(this.resource, page, limit);
  }

  create(payload: Partial<Appointment>) {
    return this.api.create<Appointment>(this.resource, payload);
  }

  update(id: number, payload: Partial<Appointment>) {
    return this.api.update<Appointment>(this.resource, id, payload);
  }

  remove(id: number) {
    return this.api.remove(this.resource, id);
  }
}
