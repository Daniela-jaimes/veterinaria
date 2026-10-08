import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { PetService } from '../../core/services/pet.service';
import { Pet } from '../../core/models/entities.models';

@Component({
  standalone: true,
  imports: [
    FormsModule
  ],
  template: `
    <!-- Encabezado -->
    <div class="page-head">

      <div>
        <h2>Mascotas</h2>

        <p class="muted">
          Pacientes vinculados a clientes.
        </p>
      </div>

      <button
        type="button"
        class="primary"
        (click)="newPet()">
        + Nueva mascota
      </button>

    </div>

    <!-- Barra de búsqueda -->
    <div class="toolbar">

      <input
        type="text"
        placeholder="Buscar por nombre"
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

    <!-- Tabla de mascotas -->
    <div class="panel table-wrap">

      <table>

        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Cliente ID</th>
            <th>Raza ID</th>
            <th>Sexo</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>

          @for (pet of items; track pet.pet_id) {

            <tr>

              <!-- ID -->
              <td>
                {{ pet.pet_id }}
              </td>

              <!-- Nombre -->
              <td>
                {{ pet.name }}
              </td>

              <!-- Cliente -->
              <td>
                {{ pet.customer_id }}
              </td>

              <!-- Raza -->
              <td>
                {{ pet.breed_id }}
              </td>

              <!-- Sexo -->
              <td>
                {{ pet.sex }}
              </td>

              <!-- Estado -->
              <td>
                <span class="badge">
                  {{ pet.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>

              <!-- Acciones -->
              <td>

                <button
                  type="button"
                  (click)="edit(pet)">
                  Editar
                </button>

                <button
                  type="button"
                  class="danger"
                  (click)="remove(pet)">
                  Desactivar
                </button>

              </td>

            </tr>

          }

          @empty {

            <tr>
              <td colspan="7">
                No hay mascotas.
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
            {{ editing ? 'Editar' : 'Nueva' }} mascota
          </h3>

          <div class="grid2">

            <!-- Cliente -->
            <label>
              Cliente ID

              <input
                type="number"
                [(ngModel)]="form.customer_id"
                name="customer_id"
                required
                min="1" />
            </label>

            <!-- Raza -->
            <label>
              Raza ID

              <input
                type="number"
                [(ngModel)]="form.breed_id"
                name="breed_id"
                required
                min="1" />
            </label>

            <!-- Nombre -->
            <label>
              Nombre

              <input
                type="text"
                [(ngModel)]="form.name"
                name="name"
                required />
            </label>

            <!-- Fecha de nacimiento -->
            <label>
              Fecha nacimiento

              <input
                type="date"
                [(ngModel)]="form.birth_date"
                name="birth_date" />
            </label>

            <!-- Sexo -->
            <label>
              Sexo

              <select
                [(ngModel)]="form.sex"
                name="sex">

                <option value="unknown">
                  Desconocido
                </option>

                <option value="male">
                  Macho
                </option>

                <option value="female">
                  Hembra
                </option>

              </select>
            </label>

            <!-- Microchip -->
            <label>
              Microchip

              <input
                type="text"
                [(ngModel)]="form.microchip_number"
                name="microchip_number" />
            </label>

            <!-- Esterilización -->
            <label class="check">

              <input
                type="checkbox"
                [(ngModel)]="form.is_neutered"
                name="is_neutered" />

              Esterilizado

            </label>

          </div>

          <!-- Acciones -->
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
export class PetsComponent {

  // Servicio de mascotas
  service = inject(PetService);

  // Lista de mascotas
  items: Pet[] = [];

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

  // Datos del formulario
  form: any = {
    customer_id: 1,
    breed_id: 1,
    name: '',
    birth_date: '',
    sex: 'unknown',
    microchip_number: '',
    is_neutered: false
  };

  constructor() {
    this.load(1);
  }

  /**
   * Cargar mascotas
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

          this.error =
            error.error?.detail ||
            'No se pudo cargar mascotas.';

        }

      });
  }

  /**
   * Abrir formulario para nueva mascota
   */
  newPet() {

    this.editing = false;

    this.form = {
      customer_id: 1,
      breed_id: 1,
      name: '',
      birth_date: '',
      sex: 'unknown',
      microchip_number: '',
      is_neutered: false
    };

    this.formOpen = true;
  }

  /**
   * Abrir formulario para editar mascota
   */
  edit(pet: Pet) {

    this.editing = true;

    this.editId = pet.pet_id;

    this.form = {
      ...pet
    };

    this.formOpen = true;
  }

  /**
   * Crear o actualizar mascota
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

        this.error =
          error.error?.detail ||
          'No se pudo guardar.';

      }

    });
  }

  /**
   * Desactivar mascota
   */
  remove(pet: Pet) {

    const confirmed = confirm(
      `¿Desactivar ${pet.name}?`
    );

    if (!confirmed) {
      return;
    }

    this.service
      .remove(pet.pet_id)
      .subscribe({

        next: () => {

          this.load(this.page);

        },

        error: (error) => {

          this.error =
            error.error?.detail ||
            'No se pudo desactivar.';

        }

      });
  }
}