"""Carga datos de ejemplo en la BD para probar la API.

Uso (desde la carpeta backend/, con el venv activo):
    python seed.py

Es idempotente: busca cada registro por su clave única antes de insertarlo,
así que se puede ejecutar varias veces sin duplicar datos.
"""
import asyncio
from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import select

from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models import (
    Appointment,
    AppUser,
    Breed,
    Consultation,
    Customer,
    MedicalRecord,
    Medication,
    Pet,
    PetAllergy,
    Speciality,
    Treatment,
    Vaccination,
    Vaccine,
    Veterinarian,
)
from app.models.enums import (
    AppointmentStatus,
    ConsultationType,
    PetSex,
    PetSpecies,
    TreatmentStatus,
    UserRole,
)

created_count = 0


async def get_or_create(session, model, lookup: dict, values: dict | None = None):
    """Devuelve el registro que cumple `lookup`; si no existe, lo crea con `lookup` + `values`."""
    global created_count
    obj = (await session.execute(select(model).filter_by(**lookup))).scalars().first()
    if obj is not None:
        return obj
    obj = model(**lookup, **(values or {}))
    session.add(obj)
    await session.flush()
    created_count += 1
    return obj


async def seed() -> None:
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    today = date.today()

    async with SessionLocal() as s:
        # --- Especialidades y veterinarios -------------------------------------------------
        general = await get_or_create(s, Speciality, {"name": "Medicina general"})
        cirugia = await get_or_create(s, Speciality, {"name": "Cirugía"})
        derma = await get_or_create(s, Speciality, {"name": "Dermatología"})

        vet1 = await get_or_create(
            s, Veterinarian, {"license_number": "MV-1001"},
            {"speciality_id": general.speciality_id, "first_name": "Laura", "last_name": "Gómez",
             "phone": "3001112233", "email": "laura.gomez@clinicavet.co"},
        )
        vet2 = await get_or_create(
            s, Veterinarian, {"license_number": "MV-1002"},
            {"speciality_id": cirugia.speciality_id, "first_name": "Andrés", "last_name": "Rojas",
             "phone": "3004445566", "email": "andres.rojas@clinicavet.co"},
        )
        await get_or_create(
            s, Veterinarian, {"license_number": "MV-1003"},
            {"speciality_id": derma.speciality_id, "first_name": "Marta", "last_name": "Ortiz",
             "phone": "3007778899", "email": "marta.ortiz@clinicavet.co"},
        )

        # --- Clientes ----------------------------------------------------------------------
        c1 = await get_or_create(
            s, Customer, {"email": "juan.perez@gmail.com"},
            {"first_name": "Juan", "last_name": "Pérez", "phone": "3101234567",
             "address": "Calle 10 # 5-20, Bogotá", "emergency_contact": "3109876543"},
        )
        c2 = await get_or_create(
            s, Customer, {"email": "maria.lopez@gmail.com"},
            {"first_name": "María", "last_name": "López", "phone": "3112223344",
             "address": "Carrera 15 # 80-12, Bogotá"},
        )
        c3 = await get_or_create(
            s, Customer, {"email": "carlos.mendez@gmail.com"},
            {"first_name": "Carlos", "last_name": "Méndez", "phone": "3125556677",
             "address": "Av. 68 # 45-10, Bogotá", "emergency_contact": "3120001122"},
        )
        await get_or_create(
            s, Customer, {"email": "sofia.ramirez@gmail.com"},
            {"first_name": "Sofía", "last_name": "Ramírez", "phone": "3138889900"},
        )

        # --- Razas -------------------------------------------------------------------------
        labrador = await get_or_create(s, Breed, {"species": PetSpecies.dog, "name": "Labrador"})
        criollo = await get_or_create(s, Breed, {"species": PetSpecies.dog, "name": "Criollo"})
        poodle = await get_or_create(s, Breed, {"species": PetSpecies.dog, "name": "Poodle"})
        siames = await get_or_create(s, Breed, {"species": PetSpecies.cat, "name": "Siamés"})
        mestizo = await get_or_create(s, Breed, {"species": PetSpecies.cat, "name": "Mestizo"})
        canario = await get_or_create(s, Breed, {"species": PetSpecies.bird, "name": "Canario"})
        await get_or_create(s, Breed, {"species": PetSpecies.rabbit, "name": "Cabeza de león"})

        # --- Mascotas ----------------------------------------------------------------------
        rocky = await get_or_create(
            s, Pet, {"microchip_number": "900100000000001"},
            {"customer_id": c1.customer_id, "breed_id": labrador.breed_id, "name": "Rocky",
             "birth_date": date(2020, 3, 15), "sex": PetSex.male, "is_neutered": True},
        )
        luna = await get_or_create(
            s, Pet, {"microchip_number": "900100000000002"},
            {"customer_id": c1.customer_id, "breed_id": siames.breed_id, "name": "Luna",
             "birth_date": date(2022, 7, 1), "sex": PetSex.female, "is_neutered": False},
        )
        toby = await get_or_create(
            s, Pet, {"microchip_number": "900100000000003"},
            {"customer_id": c2.customer_id, "breed_id": criollo.breed_id, "name": "Toby",
             "birth_date": date(2019, 11, 20), "sex": PetSex.male, "is_neutered": True},
        )
        mia = await get_or_create(
            s, Pet, {"microchip_number": "900100000000004"},
            {"customer_id": c2.customer_id, "breed_id": mestizo.breed_id, "name": "Mía",
             "birth_date": date(2023, 1, 10), "sex": PetSex.female},
        )
        coco = await get_or_create(
            s, Pet, {"microchip_number": "900100000000005"},
            {"customer_id": c3.customer_id, "breed_id": poodle.breed_id, "name": "Coco",
             "birth_date": date(2021, 5, 5), "sex": PetSex.female, "is_neutered": True},
        )
        await get_or_create(
            s, Pet, {"microchip_number": "900100000000006"},
            {"customer_id": c3.customer_id, "breed_id": canario.breed_id, "name": "Piolín",
             "birth_date": date(2024, 2, 2), "sex": PetSex.unknown},
        )

        # --- Alergias e historias clínicas -------------------------------------------------
        await get_or_create(s, PetAllergy, {"pet_id": rocky.pet_id, "description": "Alergia a la penicilina"})
        await get_or_create(s, PetAllergy, {"pet_id": coco.pet_id, "description": "Dermatitis por picadura de pulga"})

        records = {}
        for pet in (rocky, luna, toby, mia, coco):
            records[pet.pet_id] = await get_or_create(
                s, MedicalRecord, {"pet_id": pet.pet_id}, {"general_notes": "Historia creada con datos de ejemplo"}
            )

        # --- Medicamentos y vacunas --------------------------------------------------------
        amoxicilina = await get_or_create(s, Medication, {"name": "Amoxicilina"}, {"description": "Antibiótico de amplio espectro"})
        meloxicam = await get_or_create(s, Medication, {"name": "Meloxicam"}, {"description": "Antiinflamatorio"})
        await get_or_create(s, Medication, {"name": "Ivermectina"}, {"description": "Antiparasitario"})

        rabia = await get_or_create(s, Vaccine, {"name": "Antirrábica", "manufacturer": "Zoetis"})
        await get_or_create(s, Vaccine, {"name": "Quíntuple canina", "manufacturer": "Boehringer Ingelheim"})
        await get_or_create(s, Vaccine, {"name": "Triple felina", "manufacturer": "MSD"})

        # --- Citas -------------------------------------------------------------------------
        # Futuras (scheduled), una cancelada y una pasada ya completada.
        await get_or_create(
            s, Appointment, {"pet_id": luna.pet_id, "vet_id": vet1.vet_id, "reason": "Seed: control de rutina"},
            {"scheduled_at": now + timedelta(days=2, hours=1), "duration_minutes": 30},
        )
        await get_or_create(
            s, Appointment, {"pet_id": toby.pet_id, "vet_id": vet2.vet_id, "reason": "Seed: revisión de cojera"},
            {"scheduled_at": now + timedelta(days=3, hours=2), "duration_minutes": 45},
        )
        await get_or_create(
            s, Appointment, {"pet_id": mia.pet_id, "vet_id": vet1.vet_id, "reason": "Seed: cita cancelada"},
            {"scheduled_at": now + timedelta(days=4), "duration_minutes": 30, "status": AppointmentStatus.cancelled},
        )
        past = await get_or_create(
            s, Appointment, {"pet_id": rocky.pet_id, "vet_id": vet1.vet_id, "reason": "Seed: chequeo anual"},
            {"scheduled_at": now - timedelta(days=7), "duration_minutes": 30,
             "status": AppointmentStatus.completed},
        )

        # --- Consulta, tratamiento y vacunación de la cita completada ---------------------
        consulta = await get_or_create(
            s, Consultation, {"appointment_id": past.appointment_id},
            {"medical_record_id": records[rocky.pet_id].medical_record_id, "vet_id": vet1.vet_id,
             "consultation_type": ConsultationType.checkup,
             "weight_kg": Decimal("28.50"), "temperature_c": Decimal("38.5"),
             "heart_rate": 90, "respiratory_rate": 24, "mucosal_state": "Rosadas",
             "anamnesis": "Control anual sin molestias.", "diagnosis": "Paciente sano",
             "prognosis": "Bueno", "next_checkup": today + timedelta(days=358)},
        )
        await get_or_create(
            s, Treatment, {"consultation_id": consulta.consultation_id, "medication_id": meloxicam.medication_id},
            {"dosage": "1 tableta", "frequency": "Cada 24 h", "start_date": today - timedelta(days=7),
             "end_date": today - timedelta(days=2), "instructions": "Dar con comida",
             "status": TreatmentStatus.completed},
        )
        await get_or_create(
            s, Vaccination, {"consultation_id": consulta.consultation_id, "vaccine_id": rabia.vaccine_id},
            {"batch_number": "LOTE-2026-01", "date_given": today - timedelta(days=7),
             "next_due_date": today + timedelta(days=358)},
        )

        # --- Usuarios (contraseña de ejemplo: Admin123!) -----------------------------------
        pwd = hash_password("Admin123!")
        await get_or_create(
            s, AppUser, {"username": "admin"},
            {"email": "admin@clinicavet.co", "password_hash": pwd, "role": UserRole.admin},
        )
        await get_or_create(
            s, AppUser, {"username": "recepcion"},
            {"email": "recepcion@clinicavet.co", "password_hash": pwd, "role": UserRole.receptionist},
        )
        await get_or_create(
            s, AppUser, {"username": "dra.gomez"},
            {"email": "dra.gomez@clinicavet.co", "password_hash": pwd, "role": UserRole.veterinarian,
             "vet_id": vet1.vet_id},
        )

        await s.commit()

    print(f"Listo: {created_count} registros nuevos (los que ya existían se omitieron).")


async def main() -> None:
    try:
        await seed()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
