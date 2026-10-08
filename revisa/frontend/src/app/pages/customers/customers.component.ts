import {
  Component,
  inject
} from '@angular/core';

import {
  FormsModule
} from '@angular/forms';

import {
  CustomerService
} from '../../core/services/customer.service';

import {
  Customer
} from '../../core/models/entities.models';

@Component({
  selector: 'app-customers',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="page-head">
      <div>
        <h2>Clientes</h2>
        <p class="muted">
          CRUD completo con búsqueda y paginación.
        </p>
      </div>

      <button
        class="primary"
        (click)="newCustomer()"
      >
        + Nuevo cliente
      </button>
    </div>

    @if(error) {
      <div class="error">
        {{ error }}
      </div>
    }

    <div class="toolbar">
      <input
        placeholder="Buscar nombre, email o teléfono"
        [(ngModel)]="search"
        (keyup.enter)="load(1)"
      >

      <button (click)="load(1)">
        Buscar
      </button>
    </div>

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
          @for(c of items; track c.customer_id) {
            <tr>
              <td>{{ c.customer_id }}</td>

              <td>
                {{ c.first_name }} {{ c.last_name }}
              </td>

              <td>
                {{ c.phone || '—' }}
              </td>

              <td>
                {{ c.email || '—' }}
              </td>

              <td>
                <span class="badge">
                  {{ c.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>

              <td>
                <button (click)="edit(c)">
                  Editar
                </button>

                <button
                  class="danger"
                  (click)="remove(c)"
                >
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

    <div class="pager">
      <button
        [disabled]="page === 1"
        (click)="load(page - 1)"
      >
        Anterior
      </button>

      <span>
        Página {{ page }} · {{ total }} registros
      </span>

      <button
        [disabled]="page * limit >= total"
        (click)="load(page + 1)"
      >
        Siguiente
      </button>
    </div>

    @if(formOpen) {
      <div class="modal">
        <form
          class="modal-card"
          (ngSubmit)="save()"
        >
          <h3>
            {{ editing ? 'Editar' : 'Nuevo' }} cliente
          </h3>

          <div class="grid2">

            <label>
              Nombre
              <input
                [(ngModel)]="form.first_name"
                name="first_name"
                required
              >
            </label>

            <label>
              Apellido
              <input
                [(ngModel)]="form.last_name"
                name="last_name"
                required
              >
            </label>

            <label>
              Teléfono
              <input
                [(ngModel)]="form.phone"
                name="phone"
              >
            </label>

            <label>
              Email
              <input
                [(ngModel)]="form.email"
                name="email"
                type="email"
              >
            </label>

            <label>
              Dirección
              <input
                [(ngModel)]="form.address"
                name="address"
              >
            </label>

            <label>
              Contacto emergencia
              <input
                [(ngModel)]="form.emergency_contact"
                name="emergency_contact"
              >
            </label>

          </div>

          <div class="actions">
            <button
              type="button"
              (click)="formOpen = false"
            >
              Cancelar
            </button>

            <button
              type="submit"
              class="primary"
            >
              Guardar
            </button>
          </div>

        </form>
      </div>
    }
  `
})
export class CustomersComponent {

  service = inject(CustomerService);

  items: Customer[] = [];

  page = 1;
  limit = 8;
  total = 0;

  search = '';
  error = '';

  formOpen = false;
  editing = false;
  editId = 0;

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

  load(p: number) {
    this.page = p;

    this.service
      .list(p, this.limit, this.search)
      .subscribe({
        next: r => {
          this.items = r.items;
          this.total = r.total;
        },

        error: e => {
          this.error = this.msg(e);
        }
      });
  }

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

  edit(c: Customer) {
    this.editing = true;
    this.editId = c.customer_id;

    this.form = {
      ...c
    };

    this.formOpen = true;
  }

  save() {
    const call = this.editing
      ? this.service.update(this.editId, this.form)
      : this.service.create(this.form);

    call.subscribe({
      next: () => {
        this.formOpen = false;
        this.load(this.page);
      },

      error: e => {
        this.error = this.msg(e);
      }
    });
  }

  remove(c: Customer) {
    if (
      confirm(
        `¿Desactivar a ${c.first_name} ${c.last_name}?`
      )
    ) {
      this.service
        .remove(c.customer_id)
        .subscribe({
          next: () => this.load(this.page),

          error: e => {
            this.error = this.msg(e);
          }
        });
    }
  }

  msg(e: any) {
    return e.status === 409
      ? 'No se puede realizar la operación por una regla de negocio.'
      : e.error?.detail || 'Ocurrió un error.';
  }
}