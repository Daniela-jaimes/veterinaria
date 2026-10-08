import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  imports: [
    FormsModule
  ],
  template: `
    <div class="login-page">

      <div class="login-card">

        <!-- Logo -->
        <div class="logo">
          🐾
        </div>

        <!-- Título -->
        <h1>
          VetCare
        </h1>

        <p>
          Inicia sesión en el sistema de clínica veterinaria.
        </p>

        <!-- Formulario -->
        <form
          (ngSubmit)="submit()">

          <!-- Usuario -->
          <label>
            Usuario

            <input
              type="text"
              name="username"
              [(ngModel)]="username"
              required
              autocomplete="username" />
          </label>

          <!-- Contraseña -->
          <label>
            Contraseña

            <input
              type="password"
              name="password"
              [(ngModel)]="password"
              required
              autocomplete="current-password" />
          </label>

          <!-- Mensaje de error -->
          @if (error) {

            <div class="error">
              {{ error }}
            </div>

          }

          <!-- Botón de inicio de sesión -->
          <button
            type="submit"
            class="primary"
            [disabled]="loading">

            {{ loading
              ? 'Ingresando...'
              : 'Iniciar sesión'
            }}

          </button>

        </form>

        <!-- Credenciales de prueba -->
        <small>
          Prueba: admin / Admin123!
        </small>

      </div>

    </div>
  `
})
export class LoginComponent {

  // Servicios
  auth = inject(AuthService);
  router = inject(Router);

  // Datos del formulario
  username = '';
  password = '';

  // Estado de la petición
  loading = false;

  // Mensaje de error
  error = '';

  /**
   * Iniciar sesión
   */
  submit() {

    this.loading = true;
    this.error = '';

    this.auth
      .login(
        this.username,
        this.password
      )
      .subscribe({

        // Login exitoso
        next: () => {

          this.router.navigate([
            '/dashboard'
          ]);

        },

        // Error durante el login
        error: (error) => {

          if (error.status === 401) {

            this.error =
              'Usuario o contraseña incorrectos.';

          } else {

            this.error =
              'No se pudo conectar con el servidor.';

          }

          this.loading = false;
        }

      });
  }
}