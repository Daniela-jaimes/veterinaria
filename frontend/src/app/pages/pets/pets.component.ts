import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { PetService } from '../../core/services/pet.service';
import { Breed, Customer, Pet } from '../../core/models/entities.models';
import { ApiService } from '../../core/services/api.service';
import { CustomerService } from '../../core/services/customer.service';

@Component({
  standalone: true,
  imports: [
    FormsModule
  ],
  template: `
    <!-- Encabezado -->
    <div class="page-head">

      <div>
        <h2>Mascotas</h2>

        <p class="muted">
          Pacientes vinculados a clientes.
        </p>
      </div>

      <button
        type="button"
        class="primary"
        (click)="newPet()">
        + Nueva mascota
      </button>

    </div>

    <!-- Barra de búsqueda -->
    <div class="toolbar">

      <input
        type="text"
        placeholder="Buscar por nombre"
        [(ngModel)]="search"
        (keyup.enter)="load(1)" />

      <button
        type="button"
        (click)="load(1)">
        Buscar
      </button>

    </div>

    <!-- Mensaje de error -->
    @if (error) {

      <div class="error">
        {{ error }}
      </div>

    }

    <!-- Filtros por especie -->
    <div class="chips">
      @for (f of speciesFilters; track f.value) {
        <button
          type="button"
          class="chip"
          [class.on]="speciesFilter === f.value"
          (click)="setSpecies(f.value)">
          {{ f.label }}
        </button>
      }
    </div>

<!-- Tarjetas de mascotas -->
    <div class="pet-grid">

      @for (pet of items; track pet.pet_id) {

        <article class="pet-card" [class.inactive]="!pet.is_active">

          <header class="pet-top">
            <img
              class="pet-photo"
              [src]="petPhoto(pet)"
              [alt]="pet.name"
              (error)="onImgError($event)"
              loading="lazy" />

            <div class="pet-title">
              <h3>
                {{ pet.name }}
                <span class="sex" [class.f]="pet.sex === 'female'" [class.m]="pet.sex === 'male'">
                  {{ pet.sex === 'female' ? '♀' : pet.sex === 'male' ? '♂' : '' }}
                </span>
              </h3>
              <small>{{ breedLabel(pet.breed_id) }}{{ pet.is_neutered ? ' • Esterilizado' : '' }}</small>
            </div>

            <span class="age">{{ age(pet.birth_date) }}</span>
          </header>

          <dl class="pet-info">
            <div>
              <dt>Propietario:</dt>
              <dd>{{ ownerName(pet.customer_id) }}</dd>
            </div>
            <div>
              <dt>Microchip:</dt>
              <dd class="mono">{{ pet.microchip_number || '—' }}</dd>
            </div>
            <div>
              <dt>Estado:</dt>
              <dd>{{ pet.is_active ? 'Activo' : 'Inactivo' }}</dd>
            </div>
          </dl>

          <footer class="pet-actions">
            <button type="button" class="link" (click)="edit(pet)">Editar</button>
            <button type="button" class="danger" (click)="remove(pet)">Desactivar</button>
          </footer>

        </article>

      }

      @empty {
        <p class="muted">No hay mascotas.</p>
      }

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

    <!-- Modal -->
    @if (formOpen) {

      <div class="modal">

        <form
          class="modal-card"
          (ngSubmit)="save()">

          <h3>
            {{ editing ? 'Editar' : 'Nueva' }} mascota
          </h3>

          <div class="grid2">

            <!-- Cliente -->
            <label>
              Cliente

              <select
                [(ngModel)]="form.customer_id"
                name="customer_id"
                required>

                @for (c of customerList; track c.customer_id) {
                  <option [ngValue]="c.customer_id">{{ c.first_name }} {{ c.last_name }}</option>
                }

              </select>
            </label>

            <!-- Raza -->
            <label>
              Raza

              <select
                [(ngModel)]="form.breed_id"
                name="breed_id"
                required>

                @for (b of breedList; track b.breed_id) {
                  <option [ngValue]="b.breed_id">{{ b.species }} • {{ b.name }}</option>
                }

              </select>
            </label>

            <!-- Nombre -->
            <label>
              Nombre

              <input
                type="text"
                [(ngModel)]="form.name"
                name="name"
                required />
            </label>

            <!-- Fecha de nacimiento -->
            <label>
              Fecha nacimiento

              <input
                type="date"
                [(ngModel)]="form.birth_date"
                name="birth_date" />
            </label>

            <!-- Sexo -->
            <label>
              Sexo

              <select
                [(ngModel)]="form.sex"
                name="sex">

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

            <!-- Microchip -->
            <label>
              Microchip

              <input
                type="text"
                [(ngModel)]="form.microchip_number"
                name="microchip_number" />
            </label>

            <!-- Foto -->
            <label>
              Foto

              <select
                [(ngModel)]="form.photo_url"
                name="photo_url">

                <option [ngValue]="null">Sin foto</option>

                @for (img of photoOptions; track img) {
                  <option [value]="photoBase + img">{{ img }}</option>
                }

                @if (form.photo_url && !isKnownPhoto(form.photo_url)) {
                  <option [value]="form.photo_url">{{ form.photo_url }}</option>
                }

              </select>
            </label>

            @if (form.photo_url) {
              <img
                [src]="photoSrc(form.photo_url)"
                alt="Vista previa"
                (error)="onImgError($event)"
                style="width:72px;height:72px;border-radius:12px;object-fit:cover;" />
            }

            <!-- Esterilización -->
            <label class="check">

              <input
                type="checkbox"
                [(ngModel)]="form.is_neutered"
                name="is_neutered" />

              Esterilizado

            </label>

          </div>

          <!-- Acciones -->
          <div class="actions">

            <button
              type="button"
              (click)="formOpen = false">
              Cancelar
            </button>

            <button
              type="submit"
              class="primary">
              Guardar
            </button>

          </div>

        </form>

      </div>

    }
  `,
  styles: [`
    .pet-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 18px; }
    .pet-card { background: #fff; border: 1px solid #e4e8f0; border-radius: 16px; padding: 18px;
      box-shadow: 0 3px 15px #1720330a; display: flex; flex-direction: column; gap: 14px;
      transition: transform .15s, box-shadow .15s; }
    .pet-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px #17203314; }
    .pet-card.inactive { opacity: .6; }
    .pet-top { display: flex; align-items: center; gap: 12px; height: auto; padding: 0; border: 0; background: none; }
    .pet-photo { width: 56px; height: 56px; border-radius: 12px; object-fit: cover; flex-shrink: 0; background: #e2e8f0; }
    .pet-title { flex: 1; min-width: 0; }
    .pet-title h3 { margin: 0; font-size: 17px; }
    .pet-title small { color: #697386; font-size: 12px; }
    .sex { font-weight: 700; margin-left: 4px; }
    .sex.f { color: #db2777; }
    .sex.m { color: #2563eb; }
    .age { background: #f1f5f9; color: #475569; font-size: 12px; font-weight: 600; padding: 4px 9px; border-radius: 8px; align-self: flex-start; }
    .pet-info { margin: 0; border-top: 1px solid #edf0f5; padding-top: 12px; display: flex; flex-direction: column; gap: 8px; font-size: 13px; }
    .pet-info div { display: flex; justify-content: space-between; gap: 8px; }
    .pet-info dt { color: #697386; }
    .pet-info dd { margin: 0; font-weight: 600; }
    .mono { font-family: Consolas, monospace; font-size: 12px; }
    .pet-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: auto; }
    .pet-actions button { padding: 6px 12px; font-size: 13px; }
    .chips { display: flex; gap: 8px; margin-bottom: 18px; flex-wrap: wrap; }
    .chip { border-radius: 999px; padding: 6px 14px; font-size: 13px; }
    .chip.on { background: #059669; border-color: #059669; color: #fff; }
  `],
})
export class PetsComponent {

  // Servicio de mascotas
  service = inject(PetService);
  private api = inject(ApiService);
  private customerService = inject(CustomerService);

  // Catálogos para mostrar nombres en lugar de IDs
  breeds = new Map<number, { name: string; species: string }>();
  customers = new Map<number, string>();

  // Listas para los selects del formulario
  breedList: Breed[] = [];
  customerList: Customer[] = [];

  // Filtro por especie (se aplica sobre las mascotas cargadas)
  speciesFilter = 'all';
  readonly speciesFilters = [
    { value: 'all', label: 'Todas' },
    { value: 'dog', label: 'Perro' },
    { value: 'cat', label: 'Gato' },
    { value: 'bird', label: 'Ave' },
    { value: 'rabbit', label: 'Conejo' }
  ];

  /**
   * Cambia el filtro de especie y recarga desde el servidor
   */
  setSpecies(value: string) {
    this.speciesFilter = value;
    this.load(1);
  }

  breedLabel(id: number): string {
    const b = this.breeds.get(id);
    if (!b) {
      return `Raza #${id}`;
    }
    const sp = this.speciesFilters.find(f => f.value === b.species)?.label;
    return sp ? `${sp} • ${b.name}` : b.name;
  }

  ownerName(id: number): string {
    return this.customers.get(id) || `Cliente #${id}`;
  }

  // Lista de mascotas
  items: Pet[] = [];

  // Paginación
  page = 1;
  limit = 8;
  total = 0;

  // Búsqueda
  search = '';

  // Errores
  error = '';

  // Estado del formulario
  formOpen = false;
  editing = false;
  editId = 0;

  // Datos del formulario
  form: Partial<Pet> = {
    name: '',
    birth_date: '',
    sex: 'unknown',
    microchip_number: '',
    photo_url: null,
    is_neutered: false
  };

  // Fotos disponibles en frontend/public/images/animals
  readonly photoBase = '/images/animals/';
  readonly defaultPhoto =
    'data:image/svg+xml;utf8,' +
    encodeURIComponent(
      "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' fill='#e2e8f0'/><text x='32' y='42' font-size='30' text-anchor='middle'>🐾</text></svg>"
    );
  readonly photoOptions = [
    'bird_canario_1.jpg',
    'bird_canario_2.jpg',
    'cat_maine_coon.jpg',
    'cat_mestizo_1.jpg',
    'cat_persa_1.jpg',
    'cat_siame_1.jpg',
    'cat_siame_2.jpg',
    'cat_siame_3.jpg',
    'dog_buldog_1.jpg',
    'dog_criollo_1.jpg',
    'dog_golden_1.jpg',
    'dog_labrador_1.jpg',
    'dog_labrador_r_1.jpg',
    'dog_labrador_r_2.jpg',
    'dog_labrador_r_3.jpg',
    'dog_pastor_aleman_1.jpg',
    'dog_poodle_1.jpg',
    'rabbit_h_1.jpg',
    'reptile_tortuga_de_oreja_roja_1.jpg'
  ];

  // Nombres antiguos -> nombres actuales
  private readonly legacyNames: Record<string, string> = {
    'canario_1.jpg': 'bird_canario_1.jpg',
    'canarios_2.jpg': 'bird_canario_2.jpg',
    'cat_siames_2.jpg': 'cat_siame_2.jpg',
    'cat_siames_3.jpg': 'cat_siame_3.jpg',
    'tortuga_de_oreja_roja_1.jpg': 'reptile_tortuga_de_oreja_roja_1.jpg'
  };

  /**
   * Normaliza la URL de la foto a la carpeta/nombre actuales
   */
  photoSrc(url?: string | null): string {
    if (!url) {
      return this.defaultPhoto;
    }
    if (/^(https?:|data:)/.test(url)) {
      return url;
    }
    const file = url.split('/').pop() || '';
    return this.photoBase + (this.legacyNames[file] || file);
  }

  isKnownPhoto(url?: string | null): boolean {
    return !!url && url === this.photoSrc(url) && this.photoOptions.some(o => this.photoBase + o === url);
  }

  /**
   * Si la imagen no carga, usar la imagen por defecto (una sola vez para evitar bucles)
   */
  onImgError(event: Event) {
    const img = event.target as HTMLImageElement;
    if (img.src !== this.defaultPhoto) {
      img.src = this.defaultPhoto;
    }
  }

  /**
   * Edad legible a partir de la fecha de nacimiento
   */
  age(birth?: string | null): string {
    if (!birth) {
      return '—';
    }
    const b = new Date(birth);
    const now = new Date();
    let months = (now.getFullYear() - b.getFullYear()) * 12 + (now.getMonth() - b.getMonth());
    if (now.getDate() < b.getDate()) {
      months--;
    }
    if (months < 12) {
      return `${Math.max(months, 0)} ${months === 1 ? 'mes' : 'meses'}`;
    }
    const years = Math.floor(months / 12);
    return `${years} ${years === 1 ? 'año' : 'años'}`;
  }

  // Imagen sugerida por raza (palabra clave -> archivos)
  private readonly breedImages: [string, string[]][] = [
    ['bulldog', ['dog_buldog_1.jpg']],
    ['buldog', ['dog_buldog_1.jpg']],
    ['poodle', ['dog_poodle_1.jpg']],
    ['labrador', ['dog_labrador_1.jpg', 'dog_labrador_r_1.jpg', 'dog_labrador_r_2.jpg', 'dog_labrador_r_3.jpg']],
    ['golden', ['dog_golden_1.jpg']],
    ['pastor', ['dog_pastor_aleman_1.jpg']],
    ['criollo', ['dog_criollo_1.jpg']],
    ['siam', ['cat_siame_1.jpg', 'cat_siame_2.jpg', 'cat_siame_3.jpg']],
    ['persa', ['cat_persa_1.jpg']],
    ['maine', ['cat_maine_coon.jpg']],
    ['mestizo', ['cat_mestizo_1.jpg']],
    ['canario', ['bird_canario_1.jpg', 'bird_canario_2.jpg']],
    ['holand', ['rabbit_h_1.jpg']],
    ['tortuga', ['reptile_tortuga_de_oreja_roja_1.jpg']]
  ];

  private readonly speciesImages: Record<string, string> = {
    dog: 'dog_criollo_1.jpg',
    cat: 'cat_mestizo_1.jpg',
    bird: 'bird_canario_1.jpg',
    rabbit: 'rabbit_h_1.jpg',
    reptile: 'reptile_tortuga_de_oreja_roja_1.jpg'
  };

  /**
   * Foto de la mascota: la guardada, o una elegida según su raza/especie
   */
  petPhoto(pet: Pet): string {
    if (pet.photo_url) {
      return this.photoSrc(pet.photo_url);
    }
    const breed = this.breeds.get(pet.breed_id);
    if (!breed) {
      return this.defaultPhoto;
    }
    const name = breed.name.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const match = this.breedImages.find(([key]) => name.includes(key));
    if (match) {
      return this.photoBase + match[1][pet.pet_id % match[1].length];
    }
    const file = this.speciesImages[breed.species];
    return file ? this.photoBase + file : this.defaultPhoto;
  }

  constructor() {
    this.load(1);

    this.api.list<Breed>('breeds', 1, 100).subscribe({
      next: r => {
        this.breedList = r.items;
        r.items.forEach(b =>
          this.breeds.set(b.breed_id, { name: b.name, species: b.species }));
      },
      error: () => {}
    });

    this.customerService.list(1, 100).subscribe({
      next: r => {
        this.customerList = r.items;
        r.items.forEach(c =>
          this.customers.set(c.customer_id, `${c.first_name} ${c.last_name}`));
      },
      error: () => {}
    });
  }

  /**
   * Cargar mascotas
   */
  load(page: number) {

    this.page = page;

    this.service
      .list(
        page,
        this.limit,
        this.search,
        this.speciesFilter === 'all' ? '' : this.speciesFilter
      )
      .subscribe({

        next: (response) => {

          this.items = response.items;
          this.total = response.total;
          this.error = '';

        },

        error: (error: HttpErrorResponse) => {

          this.error =
            error.error?.detail ||
            'No se pudo cargar mascotas.';

        }

      });
  }

  /**
   * Abrir formulario para nueva mascota
   */
  newPet() {

    this.editing = false;

    this.form = {
      name: '',
      birth_date: '',
      sex: 'unknown',
      microchip_number: '',
      photo_url: null,
      is_neutered: false
    };

    this.formOpen = true;
  }

  /**
   * Abrir formulario para editar mascota
   */
  edit(pet: Pet) {

    this.editing = true;

    this.editId = pet.pet_id;

    this.form = {
      ...pet,
      photo_url: pet.photo_url ? this.photoSrc(pet.photo_url) : null
    };

    this.formOpen = true;
  }

  /**
   * Crear o actualizar mascota
   */
  save() {

    const request = this.editing
      ? this.service.update(
          this.editId,
          this.form
        )
      : this.service.create(
          this.form
        );

    request.subscribe({

      next: () => {

        this.formOpen = false;
        this.error = '';

        this.load(this.page);

      },

      error: (error: HttpErrorResponse) => {

        this.error =
          error.error?.detail ||
          'No se pudo guardar.';

      }

    });
  }

  /**
   * Desactivar mascota
   */
  remove(pet: Pet) {

    const confirmed = confirm(
      `¿Desactivar ${pet.name}?`
    );

    if (!confirmed) {
      return;
    }

    this.service
      .remove(pet.pet_id)
      .subscribe({

        next: () => {

          this.load(this.page);

        },

        error: (error: HttpErrorResponse) => {

          this.error =
            error.error?.detail ||
            'No se pudo desactivar.';

        }

      });
  }
}
