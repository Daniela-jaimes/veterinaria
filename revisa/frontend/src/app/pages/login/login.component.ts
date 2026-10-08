import {
  Component,
  inject
} from '@angular/core';

import {
  FormsModule
} from '@angular/forms';

import {
  Router
} from '@angular/router';

import {
  AuthService
} from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule
  ],
  template: `
    <div class="login-page">

      <div class="login-card">

        <div class="logo">
          🐾
        </div>

        <h1>VetCare</h1>

        <p>
          Inicia sesión en el sistema de clínica veterinaria.
        </p>

        <form (ngSubmit)="submit()">

          <label>
            Usuario

            <input
              name="username"
              [(ngModel)]="username"
              required
              autocomplete="username"
            >
          </label>

          <label>
            Contraseña

            <input
              name="password"
              [(ngModel)]="password"
              type="password"
              required
              autocomplete="current-password"
            >
          </label>

          @if(error) {
            <div class="error">
              {{ error }}
            </div>
          }

          <button
            class="primary"
            type="submit"
            [disabled]="loading"
          >
            {{ loading ? 'Ingresando...' : 'Iniciar sesión' }}
          </button>

        </form>

        <small>
          Prueba: admin / Admin123!
        </small>

      </div>

    </div>
  `
})
export class LoginComponent {

  auth = inject(AuthService);

  router = inject(Router);

  username = '';

  password = '';

  loading = false;

  error = '';

  submit() {

    this.loading = true;

    this.error = '';

    this.auth
      .login(this.username, this.password)
      .subscribe({

        next: () => {
          this.router.navigate([
            '/dashboard'
          ]);
        },

        error: e => {

          this.error =
            e.status === 401
              ? 'Usuario o contraseña incorrectos'
              : 'No se pudo conectar con el servidor';

          this.loading = false;

        }

      });

  }

}