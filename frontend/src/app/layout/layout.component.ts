import {
    Component,inject
} 
from '@angular/core'; 
import {
    Router,RouterLink,RouterLinkActive,RouterOutlet
} 
from '@angular/router'; 
import {
    AuthService
} 
from '../core/services/auth.service';
@Component(
    {standalone:true,imports:[RouterOutlet,RouterLink,RouterLinkActive],template:`
        <div class="shell">
            <aside>
                <h1>🐾 VetCare</h1>
                <p class="muted">Gestión veterinaria</p>
                <nav>
                    <a routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
                    <a routerLink="/customers" routerLinkActive="active">Clientes</a>
                    <a routerLink="/pets" routerLinkActive="active">Mascotas</a>
                    <a routerLink="/appointments" routerLinkActive="active">Citas</a>
                    <details open><summary>Gestión</summary>
                    <a routerLink="/veterinarians">Veterinarios</a>
                    <a routerLink="/breeds">Razas</a>
                    <a routerLink="/specialities">Especialidades</a>
                    <a routerLink="/vaccines">Vacunas</a>
                    <a routerLink="/medications">Medicamentos</a>
                    <a routerLink="/treatments">Tratamientos</a>
                    <a routerLink="/consultations">Consultas</a>
                    <a routerLink="/medical-records">Historias clínicas</a>
                    <a routerLink="/vaccinations">Vacunaciones</a>
                    <a routerLink="/pet-allergies">Alergias</a>
                    </details>@if(auth.user()?.role==='admin'){
                        <a routerLink="/users">Usuarios</a>}
                        </nav>
                        <button class="logout" (click)="logout()">Cerrar sesión</button>
                        </aside>
                        <main>
                            <header>
                                <div>
                                    <strong>Clínica Veterinaria</strong>
                                    <span class="muted"> · {{auth.user()?.username}}</span>
                                    </div>
                                    <span class="badge">{{auth.user()?.role}}</span>
                                    </header>
                                    <section class="content"><router-outlet /></section>
                                    </main>
                                    </div>`
                                    }
                                ) 
                                export class LayoutComponent {
                                    auth=inject(AuthService); 
                                    router=inject(Router); 
                                    logout(){this.auth.logout();
                                        this.router.navigate(['/login']);
                                    }
                                }
