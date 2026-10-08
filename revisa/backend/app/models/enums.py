import enum


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    in_consultation = "in_consultation"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class TreatmentStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    suspended = "suspended"


class PetSex(str, enum.Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class PetSpecies(str, enum.Enum):
    dog = "dog"
    cat = "cat"
    bird = "bird"
    rabbit = "rabbit"
    reptile = "reptile"
    rodent = "rodent"
    other = "other"


class ConsultationType(str, enum.Enum):
    checkup = "checkup"
    vaccination = "vaccination"
    emergency = "emergency"
    surgery = "surgery"
    follow_up = "follow_up"
    other = "other"


class UserRole(str, enum.Enum):
    admin = "admin"
    veterinarian = "veterinarian"
    receptionist = "receptionist"
