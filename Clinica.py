from dataclasses import dataclass
from datetime import datetime

@dataclass
class Paciente:
    _dni: str
    nombre: str
    fecha_nacimiento: str  # Formato: dd/mm/aaaa

    def obtener_dni(self) -> str:
        return self._dni

    def obtener_edad(self) -> int:
        fecha_nac = datetime.strptime(self.fecha_nacimiento, "%d/%m/%Y")
        hoy = datetime.today()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        return edad

    def _str_(self) -> str:
        return f"Paciente: {self.nombre}, con DNI: {self._dni}, nació el: {self.fecha_nacimiento}"


@dataclass
class Medico:
    matricula: str
    nombre: str
    especialidad: str

    def obtener_matricula(self) -> str:
        return self.matricula

    def _str_(self) -> str:
        return f"Médico: {self.nombre}, Matrícula: {self.matricula}, Especialidad: {self.especialidad}"

@dataclass
class Turno:
    __paciente: Paciente
    __medico: Medico
    __fecha_hora: datetime

    def obtener_fecha_hora(self) -> str:
        return self.__fecha_hora.strftime("%d/%m/%Y %H:%M")

    def _str_(self) -> str:
        return f"Turno:\nPaciente: {self._paciente.nombre}, Médico: {self._medico.nombre}, Fecha y Hora: {self.obtener_fecha_hora()}"

@dataclass
class Receta:
    __paciente: Paciente
    __medico: Medico
    __medicamentos: list[str]

    def _str_(self) -> str:
        medicamentos_str = ", ".join(self.__medicamentos)
        return f"Receta:\nPaciente: {self._paciente.nombre}, Médico: {self._medico.nombre}, Medicamentos: {medicamentos_str}"


@dataclass
class HistoriaClinica:
    __paciente: Paciente
    __turnos: list[Turno]
    __recetas: list[Receta]

    def _init_(self, paciente: Paciente):
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []

    def agregar_turno(self, turno: Turno) -> None:
        self.__turnos.append(turno)

    def agregar_receta(self, receta: Receta) -> None:
        self.__recetas.append(receta)

    def obtener_turnos(self) -> list[Turno]:
        return self.__turnos

    def obtener_recetas(self) -> list[Receta]:
        return self.__recetas

class Clinica:
    def _init_(self):
        self.__pacientes = {}
        self.__medicos = {}
        self.__turnos = []
        self.__historias_clinicas = {}

    def agregar_paciente(self, paciente: Paciente) -> None:
        self.__pacientes[paciente.obtener_dni()] = paciente
        self.__historias_clinicas[paciente.obtener_dni()] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico) -> None:
        self.__medicos[medico.obtener_matricula()] = medico

    def agendar_turno(self, dni: str, matricula: str, fecha_hora: datetime) -> None:
        paciente = self.__pacientes.get(dni)
        medico = self.__medicos.get(matricula)

        # Validar que paciente y médico existen
        if not paciente:
            print("Error: El paciente no existe.")
            return
        if not medico:
            print("Error: El médico no existe.")
            return

        # Validar que el turno no esté en el pasado
        if fecha_hora < datetime.now():
            print("Error: No se pueden agendar turnos en el pasado.")
            return

        # Validar que el médico no tenga otro turno en la misma fecha y hora
        for turno in self.__turnos:
            if turno.obtener_fecha_hora() == fecha_hora.strftime("%d/%m/%Y %H:%M") and turno.Turno_medico == medico:
                print("Error: El médico ya tiene un turno en este horario.")
                return

        # Agregar el turno si todas las validaciones pasan
        turno = Turno(__paciente=paciente, __medico=medico, __fecha_hora=fecha_hora)
        self.__turnos.append(turno)
        self.__historias_clinicas[dni].agregar_turno(turno)
        print("Turno agendado correctamente.")

# ****** Ejemplo de uso ******
paciente = Paciente(_dni="12345678", nombre="Juan Pérez", fecha_nacimiento="15/04/1990")
medico = Medico(matricula="MP12345", nombre="Dra. Martínez", especialidad="Cardiología")

turno = Turno(__paciente=paciente, __medico=medico, __fecha_hora=datetime(2025, 6, 3, 10, 30))
receta = Receta(__paciente=paciente, __medico=medico, __medicamentos=["Ibuprofeno", "Paracetamol"])

print(turno)  # Imprime el turno con fecha y hora formateada
print(receta)  # Imprime la receta con la lista de medicamentos

paciente = Paciente(_dni="12345678", nombre="Juan Pérez", fecha_nacimiento="15/04/1990")

print(f"Paciente: {paciente.nombre}, DNI: {paciente.obtener_dni()}, Edad: {paciente.obtener_edad()} años")

medico = Medico(matricula="MP12345", nombre="Dra. Martínez", especialidad="Cardiología")

print(medico)  # Esto imprimirá la representación en cadena
print(f"Matrícula: {medico.obtener_matricula()}")  # Obtiene la matrícula


paciente = Paciente(_dni="12345678", nombre="Juan Pérez", fecha_nacimiento="15/04/1990")
historia = HistoriaClinica(paciente)

medico = Medico(matricula="MP12345", nombre="Dra. Martínez", especialidad="Cardiología")
turno = Turno(__paciente=paciente, __medico=medico, __fecha_hora=datetime(2025, 6, 3, 10, 30))
receta = Receta(__paciente=paciente, __medico=medico, __medicamentos=["Ibuprofeno", "Paracetamol"])

historia.agregar_turno(turno)
historia.agregar_receta(receta)

print("Turnos registrados:")
for t in historia.obtener_turnos():
    print(t)

print("\nRecetas registradas:")
for r in historia.obtener_recetas():
    print(r)

# ***** Ejemplo de uso para clinica ******
clinica = Clinica()
paciente = Paciente(_dni="12345678", nombre="Juan Pérez", fecha_nacimiento="15/04/1990")
medico = Medico(matricula="MP12345", nombre="Dra. Martínez", especialidad="Cardiología")

clinica.agregar_paciente(paciente)
clinica.agregar_medico(medico)

# Caso de turno válido
clinica.agendar_turno("12345678", "MP12345", datetime(2025, 6, 3, 10, 30))

# Caso de turno en el pasado
clinica.agendar_turno("12345678", "MP12345", datetime(2024, 6, 3, 10, 30))

# Caso de médico con turno duplicado
clinica.agendar_turno("12345678", "MP12345", datetime(2025, 6, 3, 10, 30))