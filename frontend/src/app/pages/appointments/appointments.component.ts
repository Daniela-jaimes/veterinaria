import { Component, inject } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AppointmentService } from '../../core/services/appointment.service';
import { Appointment } from '../../core/models/entities.models';

@Component({
  standalone: true,
  imports: [
    FormsModule,
    DatePipe
  ],
  template: `
    <div class="page-head">
      <div>
        <h2>Citas</h2>
        <p class="muted">
          Agenda y estados de las citas veterinarias.
        </p>
      </div>

      <button
        class="primary"
        type="button"
        (click)="newA()">
        + Nueva cita
      </button>
    </div>

    <!-- Mensaje de error -->
    @if (error) {
      <div class="error">
        {{ error }}
      </div>
    }

    <!-- Tabla de citas -->
    <div class="panel table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Fecha</th>
            <th>Mascota</th>
            <th>Veterinario</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          @for (a of items; track a.appointment_id) {
            <tr>
              <td>
                {{ a.appointment_id }}
              </td>

              <td>
                {{ a.scheduled_at | date:'short' }}
              </td>

              <td>
                {{ a.pet_id }}
              </td>

              <td>
                {{ a.vet_id }}
              </td>

              <td>
                <span class="badge">
                  {{ a.status }}
                </span>
              </td>

              <td>
                <button
                  type="button"
                  (click)="edit(a)">
                  Editar
                </button>

                <button
                  type="button"
                  class="danger"
                  (click)="remove(a)">
                  Cancelar
                </button>
              </td>
            </tr>
          }

          @empty {
            <tr>
              <td colspan="6">
                No hay citas.
              </td>
            </tr>
          }
        </tbody>
      </table>
    </div>

    <!-- Paginación -->
    <div class="pager">
      <button
        type="button"
        [disabled]="page === 1"
        (click)="load(page - 1)">
        Anterior
      </button>

      <span>
        Página {{ page }} · {{ total }} registros
      </span>

      <button
        type="button"
        [disabled]="page * limit >= total"
        (click)="load(page + 1)">
        Siguiente
      </button>
    </div>

    <!-- Modal -->
    @if (formOpen) {
      <div class="modal">
        <form
          class="modal-card"
          (ngSubmit)="save()">

          <h3>
            {{ editing ? 'Editar' : 'Nueva' }} cita
          </h3>

          <div class="grid2">

            <!-- Mascota -->
            <label>
              Mascota ID

              <input
                type="number"
                [(ngModel)]="form.pet_id"
                name="pet_id"
                required />
            </label>

            <!-- Veterinario -->
            <label>
              Veterinario ID

              <input
                type="number"
                [(ngModel)]="form.vet_id"
                name="vet_id"
                required />
            </label>

            <!-- Fecha -->
            <label>
              Fecha y hora

              <input
                type="datetime-local"
                [(ngModel)]="form.scheduled_at"
                name="scheduled_at"
                required />
            </label>

            <!-- Motivo -->
            <label>
              Motivo

              <input
                type="text"
                [(ngModel)]="form.reason"
                name="reason"
                required />
            </label>

            <!-- Estado -->
            <label>
              Estado

              <select
                [(ngModel)]="form.status"
                name="status">

                <option value="scheduled">
                  Programada
                </option>

                <option value="in_consultation">
                  En consulta
                </option>

                <option value="completed">
                  Completada
                </option>

                <option value="cancelled">
                  Cancelada
                </option>

                <option value="no_show">
                  No asistió
                </option>
              </select>
            </label>

            <!-- Notas -->
            <label>
              Notas

              <input
                type="text"
                [(ngModel)]="form.notes"
                name="notes" />
            </label>

          </div>

          <!-- Acciones del formulario -->
          <div class="actions">

            <button
              type="button"
              (click)="formOpen = false">
              Cancelar
            </button>

            <button
              type="submit"
              class="primary">
              Guardar
            </button>

          </div>
        </form>
      </div>
    }
  `
})
export class AppointmentsComponent {

  // Servicio para comunicarse con la API
  service = inject(AppointmentService);

  // Lista de citas
  items: Appointment[] = [];

  // Paginación
  page = 1;
  limit = 8;
  total = 0;

  // Errores
  error = '';

  // Control del formulario
  formOpen = false;
  editing = false;
  editId = 0;

  // Datos del formulario
  form: any = {
    pet_id: 1,
    vet_id: 1,
    scheduled_at: '',
    reason: '',
    status: 'scheduled',
    notes: ''
  };

  constructor() {
    this.load(1);
  }

  /**
   * Cargar citas
   */
  load(page: number) {
    this.page = page;

    this.service
      .list(page, this.limit)
      .subscribe({
        next: (response) => {
          this.items = response.items;
          this.total = response.total;
          this.error = '';
        },

        error: (error) => {
          this.error =
            error.error?.detail ||
            'No se pudo cargar citas.';
        }
      });
  }

  /**
   * Abrir formulario para nueva cita
   */
  newA() {
    this.editing = false;

    this.form = {
      pet_id: 1,
      vet_id: 1,
      scheduled_at: '',
      reason: '',
      status: 'scheduled',
      notes: ''
    };

    this.formOpen = true;
  }

  /**
   * Abrir formulario para editar una cita
   */
  edit(appointment: Appointment) {
    this.editing = true;
    this.editId = appointment.appointment_id;

    this.form = {
      ...appointment,
      scheduled_at:
        appointment.scheduled_at?.slice(0, 16)
    };

    this.formOpen = true;
  }

  /**
   * Guardar una cita
   */
  save() {

    const payload = {
      ...this.form,

      scheduled_at: this.form.scheduled_at
        ? new Date(
            this.form.scheduled_at
          ).toISOString().slice(0, 19)
        : this.form.scheduled_at
    };

    const request = this.editing
      ? this.service.update(this.editId, payload)
      : this.service.create(payload);

    request.subscribe({
      next: () => {
        this.formOpen = false;
        this.error = '';

        this.load(this.page);
      },

      error: (error) => {
        this.error =
          error.error?.detail ||
          'No se pudo guardar la cita.';
      }
    });
  }

  /**
   * Cancelar una cita
   */
  remove(appointment: Appointment) {

    const confirmed = confirm(
      '¿Cancelar esta cita?'
    );

    if (!confirmed) {
      return;
    }

    this.service
      .remove(appointment.appointment_id)
      .subscribe({
        next: () => {
          this.load(this.page);
        },

        error: (error) => {
          this.error =
            error.error?.detail ||
            'No se pudo cancelar.';
        }
      });
  }
}