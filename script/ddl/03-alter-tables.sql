-- ##################################################
-- #      VETERINARY CLINIC ALTER TABLE SCRIPT      #
-- ##################################################
-- This script contains alterations to enhance the Veterinary Clinic database structure,
-- including adding new columns, modifying constraints, and implementing additional
-- validation rules to better support clinic management requirements and improve
-- data integrity across the system.
-- Run AFTER the DDL script (veterinary_clinic_schema.sql).

-- ##################################################
-- #                ALTERATIONS                     #
-- ##################################################

-- ============================================
-- NUEVAS COLUMNAS
-- ============================================

-- Add a 'color' column to the PETS table to store coat/plumage color
-- Useful for identification alongside breed and microchip
ALTER TABLE vet_clinic.pets
ADD COLUMN color VARCHAR(50);

COMMENT ON COLUMN vet_clinic.pets.color IS 'Color del pelaje, plumaje o piel de la mascota';

-- Add a 'deceased_date' column to the PETS table to record the date of death
-- Keeps the clinical history intact while marking the patient as deceased
ALTER TABLE vet_clinic.pets
ADD COLUMN deceased_date DATE;

ALTER TABLE vet_clinic.pets
ADD CONSTRAINT chk_pet_deceased_date
CHECK (deceased_date IS NULL OR birth_date IS NULL OR deceased_date >= birth_date);

COMMENT ON COLUMN vet_clinic.pets.deceased_date IS 'Fecha de fallecimiento de la mascota (nulo si está viva)';

-- Add a 'document_number' column to the CUSTOMERS table to identify the owner
-- Required for billing and to avoid duplicate customer records
ALTER TABLE vet_clinic.customers
ADD COLUMN document_number VARCHAR(30) UNIQUE;

COMMENT ON COLUMN vet_clinic.customers.document_number IS 'Número de documento de identidad del cliente';

-- ============================================
-- CONSTRAINTS PARA CONSULTAS
-- ============================================

-- Constraint para el pronóstico
ALTER TABLE vet_clinic.consultations
ADD CONSTRAINT chk_consultation_prognosis
CHECK (prognosis IS NULL OR prognosis IN ('Favorable', 'Reservado', 'Crítico'));

-- Constraint para el estado de las mucosas
ALTER TABLE vet_clinic.consultations
ADD CONSTRAINT chk_consultation_mucosal_state
CHECK (mucosal_state IS NULL OR mucosal_state IN ('Rosadas', 'Pálidas', 'Cianóticas', 'Ictéricas', 'Congestivas'));

-- ============================================
-- CONSTRAINTS PARA CORREOS ELECTRÓNICOS
-- ============================================

-- Constraint para el formato del correo de clientes
ALTER TABLE vet_clinic.customers
ADD CONSTRAINT chk_customer_email_format
CHECK (email IS NULL OR email ~* '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$');

-- Constraint para el formato del correo de veterinarios
ALTER TABLE vet_clinic.veterinarians
ADD CONSTRAINT chk_veterinarian_email_format
CHECK (email IS NULL OR email ~* '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$');

-- ##################################################
-- #                 END OF SCRIPT                  #
-- ##################################################