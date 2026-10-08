import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { CustomerService } from '../../core/services/customer.service';
import { Customer } from '../../core/models/entities.models';

@Component({
  standalone: true,
  imports: [
    FormsModule
  ],
  template: `
    <!-- Encabezado -->
    <div class="page-head">
      <div>
        <h2>Clientes</h2>

        <p class="muted">
          CRUD completo con búsqueda y paginación.
        </p>
      </div>

      <button
        type="button"
        class="primary"
        (click)="newCustomer()">
        + Nuevo cliente
      </button>
    </div>

    <!-- Barra de búsqueda -->
    <div class="toolbar">

      <input
        type="text"
        placeholder="Buscar nombre, email o teléfono"
        [(ngModel)]="search"
        (keyup.enter)="load(1)" />

      <button
        type="button"
        (click)="load(1)">
        Buscar
      </button>

    </div>

    <!-- Mensaje de error -->
    @if (error) {
      <div class="error">
        {{ error }}
      </div>
    }

    <!-- Tabla de clientes -->
    <div class="panel table-wrap">

      <table>

        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>

          @for (customer of items; track customer.customer_id) {

            <tr>

              <!-- ID -->
              <td>
                {{ customer.customer_id }}
              </td>

              <!-- Nombre -->
              <td>
                {{ customer.first_name }}
                {{ customer.last_name }}
              </td>

              <!-- Teléfono -->
              <td>
                {{ customer.phone || '—' }}
              </td>

              <!-- Email -->
              <td>
                {{ customer.email || '—' }}
              </td>

              <!-- Estado -->
              <td>
                <span class="badge">
                  {{ customer.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>

              <!-- Acciones -->
              <td>

                <button
                  type="button"
                  (click)="edit(customer)">
                  Editar
                </button>

                <button
                  type="button"
                  class="danger"
                  (click)="remove(customer)">
                  Desactivar
                </button>

              </td>

            </tr>

          }

          @empty {

            <tr>
              <td colspan="6">
                No hay clientes.
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

    <!-- Modal del formulario -->
    @if (formOpen) {

      <div class="modal">

        <form
          class="modal-card"
          (ngSubmit)="save()">

          <h3>
            {{ editing ? 'Editar' : 'Nuevo' }} cliente
          </h3>

          <div class="grid2">

            <!-- Nombre -->
            <label>
              Nombre

              <input
                type="text"
                [(ngModel)]="form.first_name"
                name="first_name"
                required />
            </label>

            <!-- Apellido -->
            <label>
              Apellido

              <input
                type="text"
                [(ngModel)]="form.last_name"
                name="last_name"
                required />
            </label>

            <!-- Teléfono -->
            <label>
              Teléfono

              <input
                type="text"
                [(ngModel)]="form.phone"
                name="phone" />
            </label>

            <!-- Email -->
            <label>
              Email

              <input
                type="email"
                [(ngModel)]="form.email"
                name="email" />
            </label>

            <!-- Dirección -->
            <label>
              Dirección

              <input
                type="text"
                [(ngModel)]="form.address"
                name="address" />
            </label>

            <!-- Contacto de emergencia -->
            <label>
              Contacto emergencia

              <input
                type="text"
                [(ngModel)]="form.emergency_contact"
                name="emergency_contact" />
            </label>

          </div>

          <!-- Botones -->
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
export class CustomersComponent {

  // Servicio de clientes
  service = inject(CustomerService);

  // Lista de clientes
  items: Customer[] = [];

  // Paginación
  page = 1;
  limit = 8;
  total = 0;

  // Búsqueda
  search = '';

  // Errores
  error = '';

  // Estado del formulario
  formOpen = false;
  editing = false;
  editId = 0;

  // Formulario
  form: any = {
    first_name: '',
    last_name: '',
    phone: '',
    email: '',
    address: '',
    emergency_contact: ''
  };

  constructor() {
    this.load(1);
  }

  /**
   * Cargar clientes
   */
  load(page: number) {

    this.page = page;

    this.service
      .list(
        page,
        this.limit,
        this.search
      )
      .subscribe({

        next: (response) => {

          this.items = response.items;
          this.total = response.total;
          this.error = '';

        },

        error: (error) => {

          this.error = this.msg(error);

        }

      });
  }

  /**
   * Abrir formulario para nuevo cliente
   */
  newCustomer() {

    this.editing = false;

    this.form = {
      first_name: '',
      last_name: '',
      phone: '',
      email: '',
      address: '',
      emergency_contact: ''
    };

    this.formOpen = true;
  }

  /**
   * Abrir formulario para editar cliente
   */
  edit(customer: Customer) {

    this.editing = true;

    this.editId = customer.customer_id;

    this.form = {
      ...customer
    };

    this.formOpen = true;
  }

  /**
   * Crear o actualizar cliente
   */
  save() {

    const request = this.editing
      ? this.service.update(
          this.editId,
          this.form
        )
      : this.service.create(
          this.form
        );

    request.subscribe({

      next: () => {

        this.formOpen = false;
        this.error = '';

        this.load(this.page);

      },

      error: (error) => {

        this.error = this.msg(error);

      }

    });
  }

  /**
   * Desactivar cliente
   */
  remove(customer: Customer) {

    const confirmed = confirm(
      `¿Desactivar a ${customer.first_name} ${customer.last_name}?`
    );

    if (!confirmed) {
      return;
    }

    this.service
      .remove(customer.customer_id)
      .subscribe({

        next: () => {

          this.load(this.page);

        },

        error: (error) => {

          this.error = this.msg(error);

        }

      });
  }

  /**
   * Obtener mensaje de error
   */
  msg(error: any): string {

    if (error.status === 409) {
      return 'No se puede realizar la operación por una regla de negocio.';
    }

    return (
      error.error?.detail ||
      'Ocurrió un error.'
    );
  }
}