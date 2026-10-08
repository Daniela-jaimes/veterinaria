import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { ApiService } from '../../core/services/api.service';

@Component({
  standalone: true,
  template: `
    <!-- Encabezado -->
    <div class="page-head">

      <div>

        <h2>
          {{ title }}
        </h2>

        <p class="muted">
          Listado conectado al endpoint
          <code>
            /{{ resource }}
          </code>
          .
        </p>

      </div>

    </div>

    <!-- Mensaje de error -->
    @if (error) {

      <div class="error">
        {{ error }}
      </div>

    }

    <!-- Tabla -->
    <div class="panel table-wrap">

      <table>

        <thead>

          <tr>

            @for (column of columns; track column) {

              <th>
                {{ column }}
              </th>

            }

          </tr>

        </thead>

        <tbody>

          @for (item of items; track $index) {

            <tr>

              @for (column of columns; track column) {

                <td>
                  {{ format(item[column]) }}
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
  `
})
export class ResourceListComponent {

  // Servicios
  api = inject(ApiService);
  route = inject(ActivatedRoute);

  // Configuración del recurso
  resource = '';
  title = '';
  idField = 'id';

  // Datos
  items: any[] = [];
  columns: string[] = [];

  // Paginación
  page = 1;
  limit = 10;
  total = 0;

  // Errores
  error = '';

  constructor() {

    const data = this.route.snapshot.data;

    this.resource = data['resource'];
    this.title = data['title'];
    this.idField = data['idField'];

    this.load(1);
  }

  /**
   * Cargar registros
   */
  load(page: number) {

    this.page = page;

    this.api
      .list<any>(
        this.resource,
        page,
        this.limit
      )
      .subscribe({

        next: (response) => {

          this.items = response.items;
          this.total = response.total;

          /*
           * Obtiene las columnas a partir
           * del primer registro.
           *
           * Se limita a las primeras 8
           * columnas para evitar tablas
           * demasiado grandes.
           */
          this.columns = this.items.length
            ? Object.keys(
                this.items[0]
              ).slice(0, 8)
            : [];

          this.error = '';

        },

        error: (error) => {

          this.error =
            error.error?.detail ||
            'No se pudo cargar el módulo.';

        }

      });
  }

  /**
   * Formatear valores para mostrarlos
   * correctamente en la tabla.
   */
  format(value: any): string {

    if (
      value === null ||
      value === undefined
    ) {
      return '—';
    }

    if (
      typeof value === 'object'
    ) {
      return JSON.stringify(value);
    }

    return String(value);
  }
}