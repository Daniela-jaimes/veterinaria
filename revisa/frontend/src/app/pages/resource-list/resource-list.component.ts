import {
  Component,
  inject
} from '@angular/core';

import {
  ActivatedRoute
} from '@angular/router';

import {
  ApiService
} from '../../core/services/api.service';

@Component({
  selector: 'app-resource-list',
  standalone: true,
  imports: [],
  template: `
    <div class="page-head">

      <div>
        <h2>
          {{ title }}
        </h2>

        <p class="muted">
          Listado conectado al endpoint
          <code>/{{ resource }}</code>.
        </p>
      </div>

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

            @for(k of columns; track k) {

              <th>
                {{ k }}
              </th>

            }

          </tr>

        </thead>


        <tbody>

          @for(item of items; track $index) {

            <tr>

              @for(k of columns; track k) {

                <td>
                  {{ format(item[k]) }}
                </td>

              }

            </tr>

          }

          @empty {

            <tr>

              <td [attr.colspan]="columns.length">

                No hay registros.

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

  `
})
export class ResourceListComponent {

  api = inject(ApiService);

  route = inject(ActivatedRoute);


  resource = '';

  title = '';

  idField = 'id';


  items: any[] = [];

  columns: string[] = [];


  page = 1;

  limit = 10;

  total = 0;

  error = '';


  constructor() {

    const d = this.route.snapshot.data;

    this.resource = d['resource'];

    this.title = d['title'];

    this.idField = d['idField'];

    this.load(1);

  }


  load(p: number) {

    this.page = p;

    this.api
      .list<any>(
        this.resource,
        p,
        this.limit
      )
      .subscribe({

        next: r => {

          this.items = r.items;

          this.total = r.total;

          this.columns = this.items.length
            ? Object.keys(this.items[0]).slice(0, 8)
            : [];

        },

        error: e => {

          this.error =
            e.error?.detail ||
            'No se pudo cargar el módulo.';

        }

      });

  }


  format(v: any) {

    return v === null || v === undefined
      ? '—'
      : typeof v === 'object'
        ? JSON.stringify(v)
        : String(v);

  }

}