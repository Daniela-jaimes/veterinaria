import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { ApiService } from '../../core/services/api.service';

@Component({
  standalone: true,
  imports: [
    RouterLink
  ],
  template: `
    <!-- Encabezado -->
    <div class="page-head">

      <div>
        <h2>Dashboard</h2>

        <p class="muted">
          Resumen de los módulos principales.
        </p>
      </div>

    </div>

    <!-- Tarjetas principales -->
    <div class="cards">

      <!-- Clientes -->
      <a
        class="card"
        routerLink="/customers">

        <b>
          Clientes
        </b>

        <strong>
          {{ customers }}
        </strong>

        <span>
          Gestionar clientes
        </span>

      </a>

      <!-- Mascotas -->
      <a
        class="card"
        routerLink="/pets">

        <b>
          Mascotas
        </b>

        <strong>
          {{ pets }}
        </strong>

        <span>
          Gestionar pacientes
        </span>

      </a>

      <!-- Citas -->
      <a
        class="card"
        routerLink="/appointments">

        <b>
          Citas
        </b>

        <strong>
          {{ appointments }}
        </strong>

        <span>
          Agenda veterinaria
        </span>

      </a>

    </div>

    <!-- Información de arquitectura -->
    <div class="panel">

      <h3>
        Arquitectura
      </h3>

      <p>
        Angular consume la API FastAPI mediante servicios HTTP.
        El interceptor agrega automáticamente
        <code>
          Authorization: Bearer &lt;token&gt;
        </code>
        a las peticiones autenticadas y redirige al login
        ante un 401.
      </p>

    </div>
  `
})
export class DashboardComponent {

  // Servicio para comunicarse con la API
  api = inject(ApiService);

  // Contadores
  customers = 0;
  pets = 0;
  appointments = 0;

  constructor() {
    this.loadDashboard();
  }

  /**
   * Cargar los totales de los módulos
   */
  loadDashboard() {

    // Total de clientes
    this.api
      .list('customers', 1, 1)
      .subscribe({
        next: (response) => {
          this.customers = response.total;
        }
      });

    // Total de mascotas
    this.api
      .list('pets', 1, 1)
      .subscribe({
        next: (response) => {
          this.pets = response.total;
        }
      });

    // Total de citas
    this.api
      .list('appointments', 1, 1)
      .subscribe({
        next: (response) => {
          this.appointments = response.total;
        }
      });
  }
}