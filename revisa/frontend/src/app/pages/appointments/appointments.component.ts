import {
    Component,inject
} 
from '@angular/core'; 
import {
    DatePipe
} 
from '@angular/common'; 
import {
    FormsModule
} 
from '@angular/forms'; 
import {
    AppointmentService
} 
from '../../core/services/appointment.service'; 
import {
    Appointment
} 
from '../../core/models/entities.models';
@Component({
    standalone:true,imports:[FormsModule,DatePipe],template:`
    <div class="page-head"><div>
        <h2>Citas</h2>
        <p class="muted">Agenda y estados de las citas veterinarias.</p>
    </div>
    <button class="primary" (click)="newA()">+ Nueva cita</button>
</div>@if(error){
    <div class="error">{{error}}</div>}
    <div class="panel table-wrap">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Fecha</th>
                    <th>Mascota</th>
                    <th>Veterinario</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                @for(a of items; 
                track a.appointment_id){
                    <tr>
                        <td>{{
                        a.appointment_id
                        }}</td>
                        <td>{{
                        a.scheduled_at | date:'short'
                        }}</td>
                        <td>{{
                        a.pet_id}}</td>
                        <td>{{
                        a.vet_id}}</td>
                        <td>
                            <span class="badge">{{a.status}}</span>
                        </td>
                        <td>
                            <button (click)="edit(a)">Editar</button>
                            <button class="danger" (click)="remove(a)">Cancelar</button>
                        </td>
                    </tr>}@empty{<tr>
                        <td colspan="6">No hay citas.</td>
                    </tr>}
                </tbody>
            </table>
        </div>
        <div class="pager">
            <button [disabled]="page===1" (click)="load(page-1)">Anterior</button>
            <span>Página {{page}} · {{total}} registros</span>
            <button [disabled]="page*limit>=total" (click)="load(page+1)">Siguiente</button>
        </div>
    @if(formOpen){
         <div class="modal">
            <form class="modal-card" (ngSubmit)="save()">
            <h3>{{editing ? 'Editar' : 'Nueva'}} cita</h3>
            <div class="grid2">
                <label>  Mascota ID
                    <input
                        type="number"
                        [(ngModel)]="form.pet_id"
                        name="pet_id"
                        required
                    >
                </label>

                <label>
                    Veterinario ID
                    <input
                        type="number"
                        [(ngModel)]="form.vet_id"
                        name="vet_id"
                        required
                    >
                </label>

                <label>
                    Fecha y hora
                    <input
                        type="datetime-local"
                        [(ngModel)]="form.scheduled_at"
                        name="scheduled_at"
                        required
                    >
                </label>

                <label>
                    Motivo
                    <input
                        [(ngModel)]="form.reason"
                        name="reason"
                        required
                    >
                </label>

                <label>
                    Estado
                    <select [(ngModel)]="form.status" name="status">
                        <option value="scheduled">Programada</option>
                        <option value="in_consultation">En consulta</option>
                        <option value="completed">Completada</option>
                        <option value="cancelled">Cancelada</option>
                        <option value="no_show">No asistió</option>
                    </select>
                </label>

                <label>
                    Notas
                    <input
                        [(ngModel)]="form.notes"
                        name="notes"
                    >
                </label>
            </div>

            <div class="actions">
                <button
                    type="button"
                    (click)="formOpen=false"
                >
                    Cancelar
                </button>

                <button
                    type="submit"
                    class="primary"
                >
                    Guardar
                </button>
            </div>
        </form>
    </div>
}
`
})
                export class AppointmentsComponent {
                    service=inject(AppointmentService);
                    items:Appointment[]=[];
                    page=1;
                    limit=8;
                    total=0;
                    error='';
                    formOpen=false;
                    editing=false;
                    editId=0;
                    form:any={
                        pet_id:1,vet_id:1,scheduled_at:'',reason:'',status:'scheduled',notes:''
                    };
                    constructor(){
                        this.load(1)
                    }
                    load(p:number){
                        this.page=p;
                        this.service.list(p,this.limit).subscribe({
                            next:r=>{
                                this.items=r.items;this.total=r.total
                            },
                            error:e=>this.error=e.error?.detail||'No se pudo cargar citas.'})
                        }
                        newA(){
                            this.editing=false;
                            this.form={
                                pet_id:1,vet_id:1,scheduled_at:'',reason:'',status:'scheduled',notes:''
                            };
                            this.formOpen=true
                        }
                        edit(a:Appointment){
                            this.editing=true;
                            this.editId=a.appointment_id;
                            this.form={...a,scheduled_at:a.scheduled_at?.slice(0,16)};
                            this.formOpen=true}save(){
                                const payload={
                                    ...this.form,scheduled_at:this.form.scheduled_at?new 
                                    Date(this.form.scheduled_at).toISOString().slice(0,19):this.form.scheduled_at
                                };
                                const call=this.editing?this.service.update(this.editId,payload):
                                this.service.create(payload);call.subscribe({next:()=>{this.formOpen=false;
                                    this.load(this.page)
                                },
                                error:e=>this.error=e.error?.detail||'No se pudo guardar la cita.'
                            }
                            )
                        }
                        remove(a:Appointment){
                            if(confirm('¿Cancelar esta cita?'))this.service.remove(a.appointment_id).
                            subscribe({next:()=>this.load(this.page),error:e=>this.error=e.error?.detail||'No se pudo cancelar.'
                            }
                            )
                        }
                    }


