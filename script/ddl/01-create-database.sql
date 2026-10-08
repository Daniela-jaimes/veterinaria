
CREATE USER vet_admin WITH PASSWORD 'tu';


CREATE DATABASE veterinaria_db WITH 
    ENCODING='UTF8' 
    LC_COLLATE='es_CO.UTF-8' 
    LC_CTYPE='es_CO.UTF-8' 
    TEMPLATE=template0 
    OWNER = vet_admin;


GRANT ALL PRIVILEGES ON DATABASE veterinaria_db TO vet_admin;