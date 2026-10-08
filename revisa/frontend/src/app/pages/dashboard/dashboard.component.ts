import {
  Component,
  inject
} from '@angular/core';

import {
  RouterLink
} from '@angular/router';

import {
  ApiService
} from '../../core/services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    RouterLink
  ],
  template: `
    <div class="page-head">
      <div>
        <h2>Dashboard</h2>
        <p class="muted">
          Resumen de los módulos principales.
        </p>
      </div>
    </div>

    <div class="cards">

      <a
        class="card"
        routerLink="/customers"
      >
        <b>Clientes</b>
        <strong>{{ customers }}</strong>
        <span>Gestionar clientes</span>
      </a>

      <a
        class="card"
        routerLink="/pets"
      >
        <b>Mascotas</b>
        <strong>{{ pets }}</strong>
        <span>Gestionar pacientes</span>
      </a>

      <a
        class="card"
        routerLink="/appointments"
      >
        <b>Citas</b>
        <strong>{{ appointments }}</strong>
        <span>Agenda veterinaria</span>
      </a>

    </div>

    <div class="panel">
      <h3>Arquitectura</h3>

      <p>
        Angular consume la API FastAPI mediante servicios HTTP.
        El interceptor agrega automáticamente
        <code>
          Authorization: Bearer &lt;token&gt;
        </code>
        a las peticiones autenticadas y redirige al login ante un 401.
      </p>
    </div>
  `
})
export class DashboardComponent {

  api = inject(ApiService);

  customers = 0;
  pets = 0;
  appointments = 0;

  constructor() {

    this.api
      .list('customers', 1, 1)
      .subscribe(r => {
        this.customers = r.total;
      });

    this.api
      .list('pets', 1, 1)
      .subscribe(r => {
        this.pets = r.total;
      });

    this.api
      .list('appointments', 1, 1)
      .subscribe(r => {
        this.appointments = r.total;
      });

  }

}