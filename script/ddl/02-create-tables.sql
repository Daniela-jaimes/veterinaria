

CREATE SCHEMA IF NOT EXISTS vet_clinic;

COMMENT ON SCHEMA vet_clinic IS 'Esquema principal para el sistema de gestión de la clínica veterinaria';

-- ##################################################
-- #        MÓDULO DE CLIENTES - INDEPENDENT        #
-- ##################################################

-- Table: customers
-- Brief: Pet owners / guardians
CREATE TABLE IF NOT EXISTS vet_clinic.customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150) UNIQUE,
    address VARCHAR(255),
    emergency_contact VARCHAR(150),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE vet_clinic.customers IS 'Clientes: propietarios o tutores de las mascotas';
COMMENT ON COLUMN vet_clinic.customers.customer_id IS 'Identificador único del cliente';
COMMENT ON COLUMN vet_clinic.customers.first_name IS 'Nombres del cliente';
COMMENT ON COLUMN vet_clinic.customers.last_name IS 'Apellidos del cliente';
COMMENT ON COLUMN vet_clinic.customers.phone IS 'Teléfono de contacto';
COMMENT ON COLUMN vet_clinic.customers.email IS 'Correo electrónico del cliente';
COMMENT ON COLUMN vet_clinic.customers.address IS 'Dirección de residencia';
COMMENT ON COLUMN vet_clinic.customers.emergency_contact IS 'Contacto de emergencia';
COMMENT ON COLUMN vet_clinic.customers.active IS 'Borrado lógico: indica si el cliente está activo';
COMMENT ON COLUMN vet_clinic.customers.created_at IS 'Fecha y hora de registro en el sistema';

-- ##################################################
-- #       MÓDULO DE PROFESIONALES - INDEPENDENT    #
-- ##################################################

-- Table: veterinarians
-- Brief: Main entity storing veterinarian information
CREATE TABLE IF NOT EXISTS vet_clinic.veterinarians (
    vet_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    speciality VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150) UNIQUE,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE vet_clinic.veterinarians IS 'Médicos veterinarios de la clínica';
COMMENT ON COLUMN vet_clinic.veterinarians.vet_id IS 'Identificador único del veterinario';
COMMENT ON COLUMN vet_clinic.veterinarians.first_name IS 'Nombres del veterinario';
COMMENT ON COLUMN vet_clinic.veterinarians.last_name IS 'Apellidos del veterinario';
COMMENT ON COLUMN vet_clinic.veterinarians.license_number IS 'CMVP o matrícula profesional';
COMMENT ON COLUMN vet_clinic.veterinarians.speciality IS 'Especialidad del veterinario';
COMMENT ON COLUMN vet_clinic.veterinarians.phone IS 'Teléfono de contacto';
COMMENT ON COLUMN vet_clinic.veterinarians.email IS 'Correo electrónico profesional';
COMMENT ON COLUMN vet_clinic.veterinarians.active IS 'Indica si el veterinario está activo en el sistema';

-- ##################################################
-- #           MÓDULO DE MASCOTAS - CORE            #
-- ##################################################

-- Table: pets
-- Brief: Patients of the clinic
CREATE TABLE IF NOT EXISTS vet_clinic.pets (
    pet_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(20) NOT NULL CHECK (species IN ('Dog', 'Cat', 'Bird', 'Rabbit', 'Reptile', 'Rodent', 'Other')),
    breed VARCHAR(100),
    birth_date DATE,
    sex CHAR(1) NOT NULL DEFAULT 'U' CHECK (sex IN ('M', 'F', 'U')),
    microchip_number VARCHAR(50) UNIQUE,
    is_neutered BOOLEAN NOT NULL DEFAULT FALSE,
    allergies_conditions TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE vet_clinic.pets IS 'Mascotas (pacientes) de la clínica';
COMMENT ON COLUMN vet_clinic.pets.pet_id IS 'Identificador único de la mascota';
COMMENT ON COLUMN vet_clinic.pets.customer_id IS 'Referencia al propietario';
COMMENT ON COLUMN vet_clinic.pets.name IS 'Nombre de la mascota';
COMMENT ON COLUMN vet_clinic.pets.species IS 'Especie (Dog: Canino, Cat: Felino, Bird: Ave, Rabbit: Conejo, Reptile: Reptil, Rodent: Roedor, Other: Otra)';
COMMENT ON COLUMN vet_clinic.pets.breed IS 'Raza de la mascota';
COMMENT ON COLUMN vet_clinic.pets.birth_date IS 'Fecha de nacimiento (o aproximada)';
COMMENT ON COLUMN vet_clinic.pets.sex IS 'Sexo (M: Macho, F: Hembra, U: Desconocido)';
COMMENT ON COLUMN vet_clinic.pets.microchip_number IS 'Número de microchip de identificación';
COMMENT ON COLUMN vet_clinic.pets.is_neutered IS 'Indica si la mascota está esterilizada';
COMMENT ON COLUMN vet_clinic.pets.allergies_conditions IS 'Alergias y condiciones preexistentes';
COMMENT ON COLUMN vet_clinic.pets.active IS 'Borrado lógico: indica si la mascota está activa';

-- Table: medical_records
-- Brief: Lifetime clinical file of the pet (1:1 with pets)
CREATE TABLE IF NOT EXISTS vet_clinic.medical_records (
    medical_record_id SERIAL PRIMARY KEY,
    pet_id INTEGER NOT NULL UNIQUE,
    opened_on DATE NOT NULL DEFAULT CURRENT_DATE,
    general_notes TEXT
);

COMMENT ON TABLE vet_clinic.medical_records IS 'Historia clínica o expediente vitalicio de la mascota (1 a 1)';
COMMENT ON COLUMN vet_clinic.medical_records.medical_record_id IS 'Identificador único de la historia clínica';
COMMENT ON COLUMN vet_clinic.medical_records.pet_id IS 'Referencia a la mascota (única: relación 1 a 1)';
COMMENT ON COLUMN vet_clinic.medical_records.opened_on IS 'Fecha de apertura de la historia clínica';
COMMENT ON COLUMN vet_clinic.medical_records.general_notes IS 'Notas generales del expediente';

-- ##################################################
-- #          MÓDULO DE ATENCIÓN - CORE             #
-- ##################################################

-- Table: appointments
-- Brief: Scheduled appointments between pets and veterinarians
CREATE TABLE IF NOT EXISTS vet_clinic.appointments (
    appointment_id SERIAL PRIMARY KEY,
    pet_id INTEGER NOT NULL,
    vet_id INTEGER NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    reason VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'InConsultation', 'Completed', 'Cancelled', 'NoShow')),
    notes TEXT,
    CONSTRAINT chk_appointment_duration CHECK (duration_minutes > 0)
);

COMMENT ON TABLE vet_clinic.appointments IS 'Citas médicas programadas entre mascotas y veterinarios';
COMMENT ON COLUMN vet_clinic.appointments.appointment_id IS 'Identificador único de la cita';
COMMENT ON COLUMN vet_clinic.appointments.pet_id IS 'Referencia a la mascota';
COMMENT ON COLUMN vet_clinic.appointments.vet_id IS 'Referencia al veterinario';
COMMENT ON COLUMN vet_clinic.appointments.scheduled_at IS 'Fecha y hora programada de la cita';
COMMENT ON COLUMN vet_clinic.appointments.duration_minutes IS 'Duración estimada de la cita en minutos';
COMMENT ON COLUMN vet_clinic.appointments.reason IS 'Motivo de la cita';
COMMENT ON COLUMN vet_clinic.appointments.status IS 'Estado de la cita (Scheduled: Programada, InConsultation: En consulta, Completed: Completada, Cancelled: Cancelada, NoShow: No asistió)';
COMMENT ON COLUMN vet_clinic.appointments.notes IS 'Notas adicionales de la cita';

-- Table: consultations
-- Brief: Clinical encounters (vital signs, anamnesis, diagnosis). May originate from an appointment or not
CREATE TABLE IF NOT EXISTS vet_clinic.consultations (
    consultation_id SERIAL PRIMARY KEY,
    medical_record_id INTEGER NOT NULL,
    appointment_id INTEGER UNIQUE,
    vet_id INTEGER NOT NULL,
    consultation_type VARCHAR(20) NOT NULL CHECK (consultation_type IN ('Checkup', 'Vaccination', 'Emergency', 'Surgery', 'FollowUp', 'Other')),
    consultation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    weight_kg NUMERIC(5, 2),
    temperature_c NUMERIC(4, 1),
    heart_rate INTEGER,
    respiratory_rate INTEGER,
    mucosal_state VARCHAR(50),
    anamnesis TEXT,
    diagnosis TEXT,
    prognosis VARCHAR(50),
    treatment_plan TEXT,
    next_checkup DATE,
    notes TEXT,
    CONSTRAINT chk_consultation_weight CHECK (weight_kg IS NULL OR weight_kg > 0),
    CONSTRAINT chk_consultation_temperature CHECK (temperature_c IS NULL OR temperature_c BETWEEN 20 AND 50),
    CONSTRAINT chk_consultation_heart_rate CHECK (heart_rate IS NULL OR heart_rate > 0),
    CONSTRAINT chk_consultation_resp_rate CHECK (respiratory_rate IS NULL OR respiratory_rate > 0)
);

COMMENT ON TABLE vet_clinic.consultations IS 'Consultas o atenciones médicas fechadas';
COMMENT ON COLUMN vet_clinic.consultations.consultation_id IS 'Identificador único de la consulta';
COMMENT ON COLUMN vet_clinic.consultations.medical_record_id IS 'Referencia a la historia clínica';
COMMENT ON COLUMN vet_clinic.consultations.appointment_id IS 'Referencia a la cita (opcional: nulo en urgencias sin cita previa)';
COMMENT ON COLUMN vet_clinic.consultations.vet_id IS 'Referencia al veterinario que atiende';
COMMENT ON COLUMN vet_clinic.consultations.consultation_type IS 'Tipo de consulta (Checkup: Control, Vaccination: Vacunación, Emergency: Urgencia, Surgery: Cirugía, FollowUp: Seguimiento, Other: Otra)';
COMMENT ON COLUMN vet_clinic.consultations.consultation_date IS 'Fecha y hora de la consulta';
COMMENT ON COLUMN vet_clinic.consultations.weight_kg IS 'Peso en kilogramos';
COMMENT ON COLUMN vet_clinic.consultations.temperature_c IS 'Temperatura en grados Celsius';
COMMENT ON COLUMN vet_clinic.consultations.heart_rate IS 'Frecuencia cardíaca (latidos por minuto)';
COMMENT ON COLUMN vet_clinic.consultations.respiratory_rate IS 'Frecuencia respiratoria (respiraciones por minuto)';
COMMENT ON COLUMN vet_clinic.consultations.mucosal_state IS 'Estado de mucosas (rosadas, pálidas, cianóticas, etc.)';
COMMENT ON COLUMN vet_clinic.consultations.anamnesis IS 'Anamnesis: historia relatada por el tutor';
COMMENT ON COLUMN vet_clinic.consultations.diagnosis IS 'Diagnóstico (opcional: no todo control tiene diagnóstico)';
COMMENT ON COLUMN vet_clinic.consultations.prognosis IS 'Pronóstico (favorable, reservado, crítico)';
COMMENT ON COLUMN vet_clinic.consultations.treatment_plan IS 'Plan terapéutico general; las prescripciones concretas van en treatments';
COMMENT ON COLUMN vet_clinic.consultations.next_checkup IS 'Fecha del próximo control';
COMMENT ON COLUMN vet_clinic.consultations.notes IS 'Notas adicionales';

-- Table: treatments
-- Brief: Prescriptions and pharmacological treatments
CREATE TABLE IF NOT EXISTS vet_clinic.treatments (
    treatment_id SERIAL PRIMARY KEY,
    medical_record_id INTEGER NOT NULL,
    consultation_id INTEGER,
    vet_id INTEGER,
    medication_name VARCHAR(150) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE,
    instructions TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Completed', 'Suspended')),
    CONSTRAINT chk_treatment_dates CHECK (end_date IS NULL OR end_date >= start_date)
);

COMMENT ON TABLE vet_clinic.treatments IS 'Tratamientos y farmacología prescrita';
COMMENT ON COLUMN vet_clinic.treatments.treatment_id IS 'Identificador único del tratamiento';
COMMENT ON COLUMN vet_clinic.treatments.medical_record_id IS 'Referencia a la historia clínica';
COMMENT ON COLUMN vet_clinic.treatments.consultation_id IS 'Referencia a la consulta (opcional: nulo si es tratamiento externo)';
COMMENT ON COLUMN vet_clinic.treatments.vet_id IS 'Referencia al veterinario que prescribe (opcional)';
COMMENT ON COLUMN vet_clinic.treatments.medication_name IS 'Nombre del medicamento';
COMMENT ON COLUMN vet_clinic.treatments.dosage IS 'Dosis (ej. 1 tableta, 2.5 ml)';
COMMENT ON COLUMN vet_clinic.treatments.frequency IS 'Frecuencia de administración (ej. cada 12 horas)';
COMMENT ON COLUMN vet_clinic.treatments.duration IS 'Duración del tratamiento (ej. 7 días)';
COMMENT ON COLUMN vet_clinic.treatments.start_date IS 'Fecha de inicio del tratamiento';
COMMENT ON COLUMN vet_clinic.treatments.end_date IS 'Fecha de fin del tratamiento';
COMMENT ON COLUMN vet_clinic.treatments.instructions IS 'Instrucciones adicionales para el tutor';
COMMENT ON COLUMN vet_clinic.treatments.status IS 'Estado del tratamiento (Active: Activo, Completed: Completado, Suspended: Suspendido)';

-- Table: vaccines
-- Brief: Vaccination and immunization records
CREATE TABLE IF NOT EXISTS vet_clinic.vaccines (
    vaccine_id SERIAL PRIMARY KEY,
    medical_record_id INTEGER NOT NULL,
    consultation_id INTEGER,
    vet_id INTEGER,
    vaccine_name VARCHAR(150) NOT NULL,
    manufacturer VARCHAR(100),
    batch_number VARCHAR(50),
    date_given DATE NOT NULL,
    next_due_date DATE,
    notes TEXT,
    CONSTRAINT chk_vaccine_dates CHECK (next_due_date IS NULL OR next_due_date >= date_given)
);

COMMENT ON TABLE vet_clinic.vaccines IS 'Vacunación e inmunización (carnet de vacunas)';
COMMENT ON COLUMN vet_clinic.vaccines.vaccine_id IS 'Identificador único de la vacuna aplicada';
COMMENT ON COLUMN vet_clinic.vaccines.medical_record_id IS 'Referencia a la historia clínica';
COMMENT ON COLUMN vet_clinic.vaccines.consultation_id IS 'Referencia a la consulta (opcional: nulo si se ingresó desde un carnet previo)';
COMMENT ON COLUMN vet_clinic.vaccines.vet_id IS 'Referencia al veterinario que aplicó la vacuna (opcional)';
COMMENT ON COLUMN vet_clinic.vaccines.vaccine_name IS 'Nombre de la vacuna';
COMMENT ON COLUMN vet_clinic.vaccines.manufacturer IS 'Laboratorio fabricante (Zoetis, Boehringer, etc.)';
COMMENT ON COLUMN vet_clinic.vaccines.batch_number IS 'Número de lote';
COMMENT ON COLUMN vet_clinic.vaccines.date_given IS 'Fecha de aplicación';
COMMENT ON COLUMN vet_clinic.vaccines.next_due_date IS 'Fecha del próximo refuerzo';
COMMENT ON COLUMN vet_clinic.vaccines.notes IS 'Notas adicionales';

-- ##################################################
-- #            RELATIONSHIP DEFINITIONS            #
-- ##################################################

-- Relationships for PETS

ALTER TABLE vet_clinic.pets ADD CONSTRAINT fk_pets_customers
    FOREIGN KEY (customer_id) REFERENCES vet_clinic.customers (customer_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

-- Relationships for MEDICAL_RECORDS

ALTER TABLE vet_clinic.medical_records ADD CONSTRAINT fk_medical_records_pets
    FOREIGN KEY (pet_id) REFERENCES vet_clinic.pets (pet_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

-- Relationships for APPOINTMENTS

ALTER TABLE vet_clinic.appointments ADD CONSTRAINT fk_appointments_pets
    FOREIGN KEY (pet_id) REFERENCES vet_clinic.pets (pet_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE vet_clinic.appointments ADD CONSTRAINT fk_appointments_veterinarians
    FOREIGN KEY (vet_id) REFERENCES vet_clinic.veterinarians (vet_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

-- Relationships for CONSULTATIONS

ALTER TABLE vet_clinic.consultations ADD CONSTRAINT fk_consultations_medical_records
    FOREIGN KEY (medical_record_id) REFERENCES vet_clinic.medical_records (medical_record_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE vet_clinic.consultations ADD CONSTRAINT fk_consultations_appointments
    FOREIGN KEY (appointment_id) REFERENCES vet_clinic.appointments (appointment_id)
    ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE vet_clinic.consultations ADD CONSTRAINT fk_consultations_veterinarians
    FOREIGN KEY (vet_id) REFERENCES vet_clinic.veterinarians (vet_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

-- Relationships for TREATMENTS

ALTER TABLE vet_clinic.treatments ADD CONSTRAINT fk_treatments_medical_records
    FOREIGN KEY (medical_record_id) REFERENCES vet_clinic.medical_records (medical_record_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE vet_clinic.treatments ADD CONSTRAINT fk_treatments_consultations
    FOREIGN KEY (consultation_id) REFERENCES vet_clinic.consultations (consultation_id)
    ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE vet_clinic.treatments ADD CONSTRAINT fk_treatments_veterinarians
    FOREIGN KEY (vet_id) REFERENCES vet_clinic.veterinarians (vet_id)
    ON UPDATE CASCADE ON DELETE SET NULL;

-- Relationships for VACCINES

ALTER TABLE vet_clinic.vaccines ADD CONSTRAINT fk_vaccines_medical_records
    FOREIGN KEY (medical_record_id) REFERENCES vet_clinic.medical_records (medical_record_id)
    ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE vet_clinic.vaccines ADD CONSTRAINT fk_vaccines_consultations
    FOREIGN KEY (consultation_id) REFERENCES vet_clinic.consultations (consultation_id)
    ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE vet_clinic.vaccines ADD CONSTRAINT fk_vaccines_veterinarians
    FOREIGN KEY (vet_id) REFERENCES vet_clinic.veterinarians (vet_id)
    ON UPDATE CASCADE ON DELETE SET NULL;

-- ##################################################
-- #                 INDEX DEFINITIONS              #
-- ##################################################

-- Avoids double booking for a veterinarian, but allows rescheduling over cancelled appointments
CREATE UNIQUE INDEX IF NOT EXISTS uq_appointments_vet_slot
    ON vet_clinic.appointments (vet_id, scheduled_at)
    WHERE status <> 'Cancelled';

-- Indexes on foreign keys
CREATE INDEX IF NOT EXISTS idx_pets_customer ON vet_clinic.pets (customer_id);
CREATE INDEX IF NOT EXISTS idx_appointments_pet ON vet_clinic.appointments (pet_id);
CREATE INDEX IF NOT EXISTS idx_consultations_record ON vet_clinic.consultations (medical_record_id);
CREATE INDEX IF NOT EXISTS idx_consultations_vet ON vet_clinic.consultations (vet_id);
CREATE INDEX IF NOT EXISTS idx_treatments_record ON vet_clinic.treatments (medical_record_id);
CREATE INDEX IF NOT EXISTS idx_treatments_consultation ON vet_clinic.treatments (consultation_id);
CREATE INDEX IF NOT EXISTS idx_vaccines_record ON vet_clinic.vaccines (medical_record_id);
CREATE INDEX IF NOT EXISTS idx_vaccines_consultation ON vet_clinic.vaccines (consultation_id);

-- Vaccine reminders
CREATE INDEX IF NOT EXISTS idx_vaccines_next_due ON vet_clinic.vaccines (next_due_date);

-- ##################################################
-- #                 END OF SCRIPT                  #
-- ##################################################
