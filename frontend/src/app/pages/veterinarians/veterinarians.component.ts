import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../core/services/api.service';

@Component({
  standalone: true,
  imports: [
    FormsModule
  ],
  template: `
    <!-- Encabezado -->
    <div class="page-head">
      <div>
        <h2>Cuerpo Veterinario</h2>
        <p class="muted">
          Médicos especialistas y datos de contacto.
        </p>
      </div>
    </div>

    <!-- Búsqueda -->
    <div class="toolbar">
      <input
        type="text"
        placeholder="Buscar por médico, especialidad o licencia"
        [(ngModel)]="search" />
    </div>

    @if (error) {
      <div class="error">{{ error }}</div>
    }

    <!-- Tarjetas -->
    <div class="vet-grid">

      @for (vet of visible(); track vet.vet_id) {

        <article class="vet-card" [class.inactive]="!vet.is_active">

          <header class="vet-top">
            <div class="vet-avatar">{{ initials(vet) }}</div>

            <div class="vet-title">
              <h3>Dr(a). {{ vet.first_name }} {{ vet.last_name }}</h3>
              <span class="spec">{{ vet.speciality?.name }}</span>
            </div>

            <span class="status" [class.off]="!vet.is_active">
              {{ vet.is_active ? 'En servicio' : 'Inactivo' }}
            </span>
          </header>

          <dl class="vet-info">
            <div>
              <dt>Licencia</dt>
              <dd class="mono">{{ vet.license_number }}</dd>
            </div>
            <div>
              <dt>Teléfono</dt>
              <dd>{{ vet.phone || '—' }}</dd>
            </div>
            <div>
              <dt>Correo</dt>
              <dd>{{ vet.email || '—' }}</dd>
            </div>
          </dl>

          <footer class="vet-actions">
            <button type="button" class="danger" (click)="remove(vet)">Eliminar</button>
          </footer>

        </article>

      }

      @empty {
        <p class="muted">No hay veterinarios.</p>
      }

    </div>
  `,
  styles: [`
    .vet-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }
    .vet-card { background: #fff; border: 1px solid #e4e8f0; border-radius: 16px; padding: 18px;
      box-shadow: 0 3px 15px #1720330a; display: flex; flex-direction: column; gap: 14px;
      transition: transform .15s, box-shadow .15s; }
    .vet-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px #17203314; }
    .vet-card.inactive { opacity: .6; }
    .vet-top { display: flex; align-items: flex-start; gap: 12px; height: auto; padding: 0; border: 0; background: none; }
    .vet-avatar { width: 48px; height: 48px; border-radius: 14px; background: #d1fae5; color: #047857;
      display: grid; place-items: center; font-weight: 700; flex-shrink: 0; }
    .vet-title { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; align-items: flex-start; }
    .vet-title h3 { margin: 0; font-size: 16px; }
    .spec { background: #ecfdf5; color: #047857; font-size: 12px; padding: 3px 9px; border-radius: 8px; }
    .status { background: #d1fae5; color: #047857; font-size: 11px; font-weight: 700; padding: 4px 9px; border-radius: 999px; }
    .status.off { background: #f1f5f9; color: #64748b; }
    .vet-info { margin: 0; background: #f8fafc; border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 8px; font-size: 13px; }
    .vet-info div { display: flex; justify-content: space-between; gap: 8px; }
    .vet-info dt { color: #697386; }
    .vet-info dd { margin: 0; font-weight: 600; text-align: right; word-break: break-all; }
    .mono { font-family: Consolas, monospace; font-size: 12px; }
    .vet-actions { display: flex; justify-content: flex-end; margin-top: auto; }
    .vet-actions button { padding: 6px 12px; font-size: 13px; }
  `]
})
export class VeterinariansComponent {

  private api = inject(ApiService);

  items: any[] = [];
  search = '';
  error = '';

  constructor() {
    this.api.list<any>('veterinarians', 1, 100).subscribe({
      next: r => this.items = r.items,
      error: e => this.error = e.error?.detail || 'No se pudo cargar veterinarios.'
    });
  }

  /**
   * Veterinarios filtrados por el texto de búsqueda
   */
  visible(): any[] {
    const q = this.search.trim().toLowerCase();
    if (!q) {
      return this.items;
    }
    return this.items.filter(v =>
      `${v.first_name} ${v.last_name} ${v.speciality?.name ?? ''} ${v.license_number}`
        .toLowerCase()
        .includes(q)
    );
  }

  initials(v: any): string {
    return `${v.first_name?.[0] ?? ''}${v.last_name?.[0] ?? ''}`.toUpperCase();
  }

  /**
   * Eliminar veterinario
   */
  remove(v: any) {
    if (!confirm(`¿Eliminar a ${v.first_name} ${v.last_name}?`)) {
      return;
    }

    this.api.remove('veterinarians', v.vet_id).subscribe({
      next: () => {
        this.items = this.items.filter(x => x.vet_id !== v.vet_id);
        this.error = '';
      },
      error: e => this.error = e.error?.detail || 'No se pudo eliminar el veterinario.'
    });
  }
}
