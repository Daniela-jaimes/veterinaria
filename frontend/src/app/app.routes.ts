import { Routes } from '@angular/router';

import {
  authGuard,
  adminGuard
} from './core/guards/auth.guard';

export const routes: Routes = [

  // =====================================================
  // LOGIN
  // =====================================================
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.component')
        .then(m => m.LoginComponent)
  },

  // =====================================================
  // ÁREA PRIVADA
  // =====================================================
  {
    path: '',
    canActivate: [authGuard],

    loadComponent: () =>
      import('./layout/layout.component')
        .then(m => m.LayoutComponent),

    children: [

      // Redirección inicial
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      },

      // =================================================
      // DASHBOARD
      // =================================================
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./pages/dashboard/dashboard.component')
            .then(m => m.DashboardComponent)
      },

      // =================================================
      // CLIENTES
      // =================================================
      {
        path: 'customers',
        loadComponent: () =>
          import('./pages/customers/customers.component')
            .then(m => m.CustomersComponent)
      },

      // =================================================
      // MASCOTAS
      // =================================================
      {
        path: 'pets',
        loadComponent: () =>
          import('./pages/pets/pets.component')
            .then(m => m.PetsComponent)
      },

      // =================================================
      // CITAS
      // =================================================
      {
        path: 'appointments',
        loadComponent: () =>
          import('./pages/appointments/appointments.component')
            .then(m => m.AppointmentsComponent)
      },

      // =================================================
      // USUARIOS
      // Solo administradores
      // =================================================
      {
        path: 'users',
        canActivate: [adminGuard],

        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'users',
          title: 'Usuarios',
          idField: 'user_id'
        }
      },

      // =================================================
      // RAZAS
      // =================================================
      {
        path: 'breeds',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'breeds',
          title: 'Razas',
          idField: 'breed_id'
        }
      },

      // =================================================
      // VETERINARIOS
      // =================================================
      {
        path: 'veterinarians',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'veterinarians',
          title: 'Veterinarios',
          idField: 'vet_id'
        }
      },

      // =================================================
      // ESPECIALIDADES
      // =================================================
      {
        path: 'specialities',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'specialities',
          title: 'Especialidades',
          idField: 'speciality_id'
        }
      },

      // =================================================
      // VACUNAS
      // =================================================
      {
        path: 'vaccines',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'vaccines',
          title: 'Vacunas',
          idField: 'vaccine_id'
        }
      },

      // =================================================
      // MEDICAMENTOS
      // =================================================
      {
        path: 'medications',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'medications',
          title: 'Medicamentos',
          idField: 'medication_id'
        }
      },

      // =================================================
      // TRATAMIENTOS
      // =================================================
      {
        path: 'treatments',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'treatments',
          title: 'Tratamientos',
          idField: 'treatment_id'
        }
      },

      // =================================================
      // CONSULTAS
      // =================================================
      {
        path: 'consultations',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'consultations',
          title: 'Consultas',
          idField: 'consultation_id'
        }
      },

      // =================================================
      // HISTORIAS CLÍNICAS
      // =================================================
      {
        path: 'medical-records',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'medical-records',
          title: 'Historias clínicas',
          idField: 'medical_record_id'
        }
      },

      // =================================================
      // VACUNACIONES
      // =================================================
      {
        path: 'vaccinations',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'vaccinations',
          title: 'Vacunaciones',
          idField: 'vaccination_id'
        }
      },

      // =================================================
      // ALERGIAS DE MASCOTAS
      // =================================================
      {
        path: 'pet-allergies',
        loadComponent: () =>
          import('./pages/resource-list/resource-list.component')
            .then(m => m.ResourceListComponent),

        data: {
          resource: 'pet-allergies',
          title: 'Alergias',
          idField: 'allergy_id'
        }
      }
    ]
  },

  // =====================================================
  // RUTA NO ENCONTRADA
  // =====================================================
  {
    path: '**',
    redirectTo: ''
  }
];