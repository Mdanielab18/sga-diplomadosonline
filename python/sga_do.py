from collections import deque


# ============================================================
# SGA-DO: SISTEMA DIPLOMADOSONLINE
# Implementación en Python
# ============================================================

ARCHIVO_ALUMNOS = "alumnos.txt"
ARCHIVO_PROFESORES = "profesores.txt"
ARCHIVO_CERTIFICADOS = "certificados_pendientes.txt"
MAX_NOTAS = 3


# -----------------------------
# Jerarquía de Personas
# -----------------------------

class Persona:
    def __init__(self, cedula, nombre, correo):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo


class Alumno(Persona):
    def __init__(self, cedula, nombre, correo, programa, notas=None):
        super().__init__(cedula, nombre, correo)
        self.programa = programa
        self.notas = notas if notas is not None else []

    def agregar_nota(self, nota):
        if len(self.notas) >= MAX_NOTAS:
            return False

        self.notas.append(nota)
        return True

    def eliminar_ultima_nota(self):
        if not self.notas:
            return None

        # LIFO: se elimina la última nota registrada.
        return self.notas.pop()

    def promedio(self):
        if not self.notas:
            return 0

        return sum(self.notas) / len(self.notas)

    def esta_aprobado(self):
        # Se requieren las 3 notas indicadas en las reglas del proyecto.
        if len(self.notas) < MAX_NOTAS:
            return False

        return self.programa.esta_aprobado(self.notas)


class Profesor(Persona):
    def __init__(self, cedula, nombre, correo, especialidad, materia):
        super().__init__(cedula, nombre, correo)
        self.especialidad = especialidad
        self.materia = materia


# -----------------------------
# Jerarquía de Programas
# -----------------------------

class ProgramaAcademico:
    def __init__(self, nombre):
        self.nombre = nombre

    def esta_aprobado(self, notas):
        raise NotImplementedError


class Curso(ProgramaAcademico):
    def __init__(self):
        super().__init__("Curso")

    def esta_aprobado(self, notas):
        return sum(notas) / len(notas) >= 10


class Diplomado(ProgramaAcademico):
    def __init__(self):
        super().__init__("Diplomado")

    def esta_aprobado(self, notas):
        return sum(notas) / len(notas) >= 14


class Bootcamp(ProgramaAcademico):
    def __init__(self):
        super().__init__("Bootcamp")

    def esta_aprobado(self, notas):
        return all(nota >= 14 for nota in notas)


def crear_programa(nombre):
    nombre = nombre.strip().lower()

    if nombre == "curso":
        return Curso()

    if nombre == "diplomado":
        return Diplomado()

    if nombre == "bootcamp":
        return Bootcamp()

    return None


# -----------------------------
# Persistencia
# -----------------------------

def guardar_alumnos(alumnos):
    with open(ARCHIVO_ALUMNOS, "w", encoding="utf-8") as archivo:

        for alumno in alumnos.values():

            notas = alumno.notas + [0] * (MAX_NOTAS - len(alumno.notas))

            linea = (
                f"{alumno.cedula},{alumno.nombre},{alumno.correo},"
                f"{alumno.programa.nombre},{notas[0]},{notas[1]},{notas[2]}\n"
            )

            archivo.write(linea)


def guardar_profesores(profesores):
    with open(ARCHIVO_PROFESORES, "w", encoding="utf-8") as archivo:

        for profesor in profesores.values():

            linea = (
                f"{profesor.cedula},{profesor.nombre},{profesor.correo},"
                f"{profesor.especialidad},{profesor.materia}\n"
            )

            archivo.write(linea)


def cargar_alumnos():
    alumnos = {}

    try:
        with open(ARCHIVO_ALUMNOS, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                datos = linea.strip().split(",")

                if len(datos) != 7:
                    continue

                cedula, nombre, correo, tipo, n1, n2, n3 = datos

                programa = crear_programa(tipo)

                if programa is None:
                    continue

                try:
                    valores = [
                        float(n1),
                        float(n2),
                        float(n3)
                    ]

                except ValueError:
                    continue

                # Los ceros representan notas aún no registradas.
                notas = [
                    n for n in valores
                    if n != 0
                ]

                alumnos[cedula] = Alumno(
                    cedula,
                    nombre,
                    correo,
                    programa,
                    notas
                )

    except FileNotFoundError:
        pass

    return alumnos


def cargar_profesores():
    profesores = {}

    try:
        with open(ARCHIVO_PROFESORES, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                datos = linea.strip().split(",")

                if len(datos) != 5:
                    continue

                cedula, nombre, correo, especialidad, materia = datos

                profesores[cedula] = Profesor(
                    cedula,
                    nombre,
                    correo,
                    especialidad,
                    materia
                )

    except FileNotFoundError:
        pass

    return profesores


# -----------------------------
# Utilidades
# -----------------------------

def leer_nota():

    while True:

        try:
            nota = float(input("Ingrese la nota (0-20): "))

            if 0 <= nota <= 20:
                return nota

            print("La nota debe estar entre 0 y 20.")

        except ValueError:
            print("Ingrese un valor numérico válido.")


def mostrar_estado(alumno):

    if len(alumno.notas) < MAX_NOTAS:
        return "EN CURSO"

    return "APROBADO" if alumno.esta_aprobado() else "REPROBADO"


# -----------------------------
# Opciones del sistema
# -----------------------------

def registrar_alumno(alumnos):

    print("\n--- REGISTRAR ALUMNO ---")

    cedula = input("Cédula/ID: ").strip()

    if cedula in alumnos:
        print("Error: ya existe un alumno con esa Cédula/ID.")
        return

    nombre = input("Nombre completo: ").strip()
    correo = input("Correo electrónico: ").strip()

    while True:

        tipo = input(
            "Programa (Curso/Diplomado/Bootcamp): "
        ).strip()

        programa = crear_programa(tipo)

        if programa:
            break

        print(
            "Programa no válido. "
            "Seleccione Curso, Diplomado o Bootcamp."
        )

    alumnos[cedula] = Alumno(
        cedula,
        nombre,
        correo,
        programa
    )

    guardar_alumnos(alumnos)

    print("Alumno registrado correctamente en alumnos.txt.")


def registrar_profesor(profesores):

    print("\n--- REGISTRAR PROFESOR ---")

    cedula = input("Cédula/ID: ").strip()

    if cedula in profesores:
        print("Error: ya existe un profesor con esa Cédula/ID.")
        return

    nombre = input("Nombre completo: ").strip()
    correo = input("Correo electrónico: ").strip()
    especialidad = input("Especialidad académica: ").strip()
    materia = input("Materia asignada: ").strip()

    profesores[cedula] = Profesor(
        cedula,
        nombre,
        correo,
        especialidad,
        materia
    )

    guardar_profesores(profesores)

    print("Profesor registrado correctamente en profesores.txt.")


def registrar_nota(alumnos, pila_undo):

    print("\n--- REGISTRAR NOTA ---")

    cedula = input(
        "Cédula/ID del alumno: "
    ).strip()

    alumno = alumnos.get(cedula)

    if alumno is None:
        print("Alumno no encontrado.")
        return

    if len(alumno.notas) >= MAX_NOTAS:
        print("El alumno ya tiene las 3 notas permitidas.")
        return

    nota = leer_nota()

    alumno.agregar_nota(nota)

    # Se guarda la acción en la pila.
    # La pila mantiene el orden LIFO.
    pila_undo.append(
        (cedula, nota)
    )

    guardar_alumnos(alumnos)

    print(
        f"Nota registrada correctamente."
    )

    print(
        f"Alumno: {alumno.nombre}"
    )

    print(
        f"Notas actuales: {alumno.notas}"
    )


def deshacer_ultima_nota(alumnos, pila_undo):

    print("\n--- DESHACER ÚLTIMO REGISTRO DE NOTA ---")

    if not pila_undo:

        print(
            "No existen notas registradas "
            "que puedan deshacerse."
        )

        return

    # --------------------------------------------------------
    # Se solicita la cédula del alumno.
    # --------------------------------------------------------

    cedula = input(
        "Ingrese la Cédula/ID del alumno: "
    ).strip()

    alumno = alumnos.get(cedula)

    if alumno is None:

        print(
            "Alumno no encontrado."
        )

        return

    # --------------------------------------------------------
    # Verificar si el alumno tiene notas.
    # --------------------------------------------------------

    if not alumno.notas:

        print(
            f"El alumno {alumno.nombre} "
            "no tiene notas registradas."
        )

        return

    # --------------------------------------------------------
    # Mostrar información antes de eliminar.
    # --------------------------------------------------------

    print(
        f"\nAlumno encontrado: {alumno.nombre}"
    )

    print(
        f"Notas actuales: {alumno.notas}"
    )

    ultima_nota = alumno.notas[-1]

    print(
        f"Última nota del alumno: {ultima_nota}"
    )

    # --------------------------------------------------------
    # Confirmación.
    # --------------------------------------------------------

    confirmar = input(
        "¿Desea eliminar esta nota? (S/N): "
    ).strip().upper()

    if confirmar != "S":

        print(
            "Operación cancelada."
        )

        return

    # --------------------------------------------------------
    # Eliminar la última nota del alumno.
    # --------------------------------------------------------

    eliminada = alumno.eliminar_ultima_nota()

    # --------------------------------------------------------
    # Buscar en la pila la última acción correspondiente
    # a ese alumno.
    #
    # Se recorre desde el final porque la última acción
    # registrada para ese alumno debe ser la primera en
    # deshacerse: LIFO.
    # --------------------------------------------------------

    indice_en_pila = None

    for i in range(len(pila_undo) - 1, -1, -1):

        cedula_pila, nota_pila = pila_undo[i]

        if cedula_pila == cedula:

            indice_en_pila = i
            break

    # --------------------------------------------------------
    # Eliminar de la pila la acción correspondiente.
    # --------------------------------------------------------

    if indice_en_pila is not None:

        pila_undo.pop(indice_en_pila)

    # --------------------------------------------------------
    # Guardar los cambios.
    # --------------------------------------------------------

    guardar_alumnos(alumnos)

    print(
        f"\nSe eliminó correctamente la última nota "
        f"del alumno {alumno.nombre}."
    )

    print(
        f"Nota eliminada: {eliminada}"
    )

    print(
        f"Notas actuales: {alumno.notas}"
    )


def generar_cola_certificados(alumnos):

    print("\n--- GENERAR COLA DE CERTIFICADOS ---")

    # Cola FIFO.
    cola = deque()

    for alumno in alumnos.values():

        if alumno.esta_aprobado():

            cola.append(alumno)

    with open(
        ARCHIVO_CERTIFICADOS,
        "w",
        encoding="utf-8"
    ) as archivo:

        while cola:

            alumno = cola.popleft()

            archivo.write(
                f"{alumno.cedula},{alumno.nombre},"
                f"{alumno.programa.nombre},"
                f"Promedio:{alumno.promedio():.2f}\n"
            )

    cantidad = sum(
        1
        for alumno in alumnos.values()
        if alumno.esta_aprobado()
    )

    print(
        f"Proceso finalizado. Se generaron "
        f"{cantidad} certificados pendientes."
    )

    print(
        f"Archivo generado: {ARCHIVO_CERTIFICADOS}"
    )


def mostrar_reporte(alumnos, profesores):

    print("\n" + "=" * 60)

    print(
        "REPORTE GENERAL SGA-DO"
    )

    print("=" * 60)

    print("\n--- PROFESORES ACTIVOS ---")

    if not profesores:

        print(
            "No hay profesores registrados."
        )

    else:

        for profesor in profesores.values():

            print(
                f"ID: {profesor.cedula} | "
                f"Nombre: {profesor.nombre} | "
                f"Correo: {profesor.correo} | "
                f"Especialidad: {profesor.especialidad} | "
                f"Materia: {profesor.materia}"
            )

    print("\n--- ALUMNOS REGISTRADOS ---")

    if not alumnos:

        print(
            "No hay alumnos registrados."
        )

    else:

        for alumno in alumnos.values():

            notas = alumno.notas + [
                0
            ] * (
                MAX_NOTAS - len(alumno.notas)
            )

            print(
                f"ID: {alumno.cedula} | "
                f"Nombre: {alumno.nombre} | "
                f"Programa: {alumno.programa.nombre} | "
                f"Notas: {notas} | "
                f"Promedio: {alumno.promedio():.2f} | "
                f"Estatus: {mostrar_estado(alumno)}"
            )


def mostrar_menu():

    print("\n" + "=" * 50)

    print(
        "SGA-DO: SISTEMA DIPLOMADOSONLINE"
    )

    print("=" * 50)

    print("1. Registrar Alumno")
    print("2. Registrar Profesor")
    print("3. Registrar Notas a un Alumno")
    print("4. Deshacer Último Registro de Nota")
    print("5. Generar Cola de Certificados")
    print("6. Mostrar Reporte General")
    print("7. Salir")

    print("=" * 50)


# -----------------------------
# Programa principal
# -----------------------------

def main():

    # Datos persistentes cargados desde los archivos .txt.
    alumnos = cargar_alumnos()
    profesores = cargar_profesores()

    # Pila para las acciones de notas.
    # Cada elemento tiene:
    # (Cédula del alumno, nota registrada)
    pila_undo = []

    while True:

        mostrar_menu()

        opcion = input(
            "Seleccione una opción (1-7): "
        ).strip()

        if opcion == "1":

            registrar_alumno(alumnos)

        elif opcion == "2":

            registrar_profesor(profesores)

        elif opcion == "3":

            registrar_nota(
                alumnos,
                pila_undo
            )

        elif opcion == "4":

            deshacer_ultima_nota(
                alumnos,
                pila_undo
            )

        elif opcion == "5":

            generar_cola_certificados(
                alumnos
            )

        elif opcion == "6":

            mostrar_reporte(
                alumnos,
                profesores
            )

        elif opcion == "7":

            guardar_alumnos(alumnos)
            guardar_profesores(profesores)

            print(
                "\nLos cambios han sido guardados. "
                "SGA-DO cerrado de forma segura."
            )

            break

        else:

            print(
                "Opción no válida. "
                "Seleccione un número del 1 al 7."
            )


if __name__ == "__main__":
    main()