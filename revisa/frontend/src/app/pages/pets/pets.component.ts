import {
  Component,
  inject
} from '@angular/core';

import {
  FormsModule
} from '@angular/forms';

import {
  PetService
} from '../../core/services/pet.service';

import {
  Pet
} from '../../core/models/entities.models';

@Component({
  selector: 'app-pets',
  standalone: true,
  imports: [
    FormsModule
  ],
  template: `
    <div class="page-head">

      <div>
        <h2>Mascotas</h2>

        <p class="muted">
          Pacientes vinculados a clientes.
        </p>
      </div>

      <button
        class="primary"
        (click)="newPet()"
      >
        + Nueva mascota
      </button>

    </div>


    <div class="toolbar">

      <input
        placeholder="Buscar por nombre"
        [(ngModel)]="search"
        (keyup.enter)="load(1)"
      >

      <button (click)="load(1)">
        Buscar
      </button>

    </div>


    @if(error) {
      <div class="error">
        {{ error }}
      </div>
    }


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

          @for(p of items; track p.pet_id) {

            <tr>

              <td>
                {{ p.pet_id }}
              </td>

              <td>
                {{ p.name }}
              </td>

              <td>
                {{ p.customer_id }}
              </td>

              <td>
                {{ p.breed_id }}
              </td>

              <td>
                {{ p.sex }}
              </td>

              <td>
                {{ p.is_active ? 'Activo' : 'Inactivo' }}
              </td>

              <td>

                <button
                  (click)="edit(p)"
                >
                  Editar
                </button>

                <button
                  class="danger"
                  (click)="remove(p)"
                >
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
            {{ editing ? 'Editar' : 'Nueva' }} mascota
          </h3>


          <div class="grid2">

            <label>
              Cliente ID

              <input
                type="number"
                [(ngModel)]="form.customer_id"
                name="customer_id"
                required
                min="1"
              >
            </label>


            <label>
              Raza ID

              <input
                type="number"
                [(ngModel)]="form.breed_id"
                name="breed_id"
                required
                min="1"
              >
            </label>


            <label>
              Nombre

              <input
                [(ngModel)]="form.name"
                name="name"
                required
              >
            </label>


            <label>
              Fecha nacimiento

              <input
                type="date"
                [(ngModel)]="form.birth_date"
                name="birth_date"
              >
            </label>


            <label>
              Sexo

              <select
                [(ngModel)]="form.sex"
                name="sex"
              >

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


            <label>
              Microchip

              <input
                [(ngModel)]="form.microchip_number"
                name="microchip_number"
              >
            </label>


            <label class="check">

              <input
                type="checkbox"
                [(ngModel)]="form.is_neutered"
                name="is_neutered"
              >

              Esterilizado

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
export class PetsComponent {

  service = inject(PetService);

  items: Pet[] = [];

  page = 1;

  limit = 8;

  total = 0;

  search = '';

  error = '';

  formOpen = false;

  editing = false;

  editId = 0;


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


  load(p: number) {

    this.page = p;

    this.service
      .list(
        p,
        this.limit,
        this.search
      )
      .subscribe({

        next: r => {

          this.items = r.items;

          this.total = r.total;

        },

        error: e => {

          this.error =
            e.error?.detail ||
            'No se pudo cargar mascotas.';

        }

      });

  }


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


  edit(p: Pet) {

    this.editing = true;

    this.editId = p.pet_id;

    this.form = {
      ...p
    };

    this.formOpen = true;

  }


  save() {

    const call = this.editing
      ? this.service.update(
          this.editId,
          this.form
        )
      : this.service.create(
          this.form
        );


    call.subscribe({

      next: () => {

        this.formOpen = false;

        this.load(this.page);

      },

      error: e => {

        this.error =
          e.error?.detail ||
          'No se pudo guardar.';

      }

    });

  }


  remove(p: Pet) {

    if (
      confirm(
        `¿Desactivar ${p.name}?`
      )
    ) {

      this.service
        .remove(p.pet_id)
        .subscribe({

          next: () => {

            this.load(this.page);

          },

          error: e => {

            this.error =
              e.error?.detail ||
              'No se pudo desactivar.';

          }

        });

    }

  }

}