from collections import deque

# ============================================================
# SGA-DO: SISTEMA DIPLOMADOSONLINE
# Implementación en Python
# ============================================================

from pathlib import Path

CARPETA_PYTHON = Path(__file__).resolve().parent

ARCHIVO_ALUMNOS = CARPETA_PYTHON / "alumnos.txt"
ARCHIVO_PROFESORES = CARPETA_PYTHON / "profesores.txt"
ARCHIVO_CERTIFICADOS = CARPETA_PYTHON / "certificados_pendientes.txt"
MAX_NOTAS = 3


# =========================
#  Jerarquía de PERSONAS
# =========================
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
        return self.notas.pop() if self.notas else None

    def promedio(self):
        if len(self.notas) != MAX_NOTAS:
            return 0
        return sum(self.notas) / MAX_NOTAS

    def esta_aprobado(self):
        if len(self.notas) != MAX_NOTAS:
            return False
        return self.programa.esta_aprobado(self.notas)


class Profesor(Persona):
    def __init__(self, cedula, nombre, correo, especialidad, materia):
        super().__init__(cedula, nombre, correo)
        self.especialidad = especialidad
        self.materia = materia


# =========================
#  Jerarquía de PROGRAMAS 
# =========================
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


# =========================
# PERSISTENCIA
# =========================
def guardar_alumnos(alumnos):
    with open(ARCHIVO_ALUMNOS, "w", encoding="utf-8") as archivo:
        for alumno in alumnos.values():
            notas = alumno.notas + [0] * (MAX_NOTAS - len(alumno.notas))
            archivo.write(
                f"{alumno.cedula},{alumno.nombre},{alumno.correo},"
                f"{alumno.programa.nombre},{notas[0]},{notas[1]},{notas[2]}\n"
            )


def cargar_alumnos():
    alumnos = {}
    try:
        with open(ARCHIVO_ALUMNOS, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, 1):
                linea = linea.strip()
                if not linea:
                    continue
                datos = [x.strip() for x in linea.split(",")]
                if len(datos) != 7:
                    print(f"Aviso: línea {numero_linea} de alumnos.txt ignorada.")
                    continue
                cedula, nombre, correo, tipo, n1, n2, n3 = datos
                programa = crear_programa(tipo)
                if programa is None:
                    print(f"Aviso: programa inválido en línea {numero_linea}.")
                    continue
                try:
                    valores = [float(n1), float(n2), float(n3)]
                except ValueError:
                    print(f"Aviso: notas inválidas en línea {numero_linea}.")
                    continue
                # En el formato del proyecto, 0 significa nota aún no registrada.
                notas = [n for n in valores if n != 0]
                alumnos[cedula] = Alumno(cedula, nombre, correo, programa, notas)
    except FileNotFoundError:
        pass
    return alumnos


def guardar_profesores(profesores):
    with open(ARCHIVO_PROFESORES, "w", encoding="utf-8") as archivo:
        for profesor in profesores.values():
            archivo.write(
                f"{profesor.cedula},{profesor.nombre},{profesor.correo},"
                f"{profesor.especialidad},{profesor.materia}\n"
            )


def cargar_profesores():
    profesores = {}
    try:
        with open(ARCHIVO_PROFESORES, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, 1):
                linea = linea.strip()
                if not linea:
                    continue
                datos = [x.strip() for x in linea.split(",")]
                if len(datos) != 5:
                    print(f"Aviso: línea {numero_linea} de profesores.txt ignorada.")
                    continue
                cedula, nombre, correo, especialidad, materia = datos
                profesores[cedula] = Profesor(
                    cedula, nombre, correo, especialidad, materia
                )
    except FileNotFoundError:
        pass
    return profesores


# =========================
# OPCIONES
# =========================
def leer_nota():
    while True:
        try:
            nota = float(input("Ingrese la nota (0-20): "))
            if 0 <= nota <= 20:
                return nota
            print("La nota debe estar entre 0 y 20.")
        except ValueError:
            print("Ingrese un valor numérico válido.")


def registrar_alumno(alumnos):
    print("\n--- REGISTRAR ALUMNO ---")
    cedula = input("Cédula/ID: ").strip()
    if cedula in alumnos:
        print("Error: ya existe un alumno con esa Cédula/ID.")
        return
    nombre = input("Nombre completo: ").strip()
    correo = input("Correo electrónico: ").strip()
    while True:
        tipo = input("Programa (Curso/Diplomado/Bootcamp): ").strip()
        programa = crear_programa(tipo)
        if programa:
            break
        print("Programa no válido.")
    alumnos[cedula] = Alumno(cedula, nombre, correo, programa)
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
    profesores[cedula] = Profesor(cedula, nombre, correo, especialidad, materia)
    guardar_profesores(profesores)
    print("Profesor registrado correctamente en profesores.txt.")


def registrar_nota(alumnos, pila_notas):
    print("\n--- REGISTRAR NOTA ---")
    cedula = input("Cédula/ID del alumno: ").strip()
    alumno = alumnos.get(cedula)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    if len(alumno.notas) >= MAX_NOTAS:
        print("El alumno ya tiene las 3 notas permitidas.")
        return
    nota = leer_nota()
    alumno.agregar_nota(nota)
    # La PILA guarda la cédula y la nota. DESHACER no pregunta nada.
    pila_notas.append((cedula, nota))
    guardar_alumnos(alumnos)
    print(f"Nota {nota} registrada para {alumno.nombre}.")


def deshacer_ultima_nota(alumnos, pila_notas):
    print("\n--- DESHACER ÚLTIMO REGISTRO DE NOTA ---")
    # No se pide cédula: se toma automáticamente la última acción de la pila.
    if not pila_notas:
        print("No hay registros de notas para deshacer.")
        return

    # LIFO: la última nota introducida es la primera que se deshace.
    cedula, nota_registrada = pila_notas.pop()
    alumno = alumnos.get(cedula)

    if alumno is None:
        print("No se encontró el alumno asociado a la última nota.")
        return

    nota_eliminada = alumno.eliminar_ultima_nota()
    guardar_alumnos(alumnos)

    print("Deshacer realizado correctamente.")
    print(f"Alumno: {alumno.nombre}")
    print(f"Nota eliminada: {nota_eliminada}")
    print(f"Notas actuales: {alumno.notas}")


def generar_cola_certificados(alumnos):
    print("\n--- GENERAR COLA DE CERTIFICADOS ---")

    # Se recorre TODOS los alumnos cargados desde alumnos.txt.
    cola = deque()

    for alumno in alumnos.values():
        if alumno.esta_aprobado():
            cola.append(alumno)

    # FIFO: el primero que entra es el primero que sale.
    certificados = []
    while cola:
        alumno = cola.popleft()
        certificados.append(
            f"{alumno.cedula},{alumno.nombre},{alumno.programa.nombre},"
            f"Promedio:{alumno.promedio():.2f}"
        )

    with open(ARCHIVO_CERTIFICADOS, "w", encoding="utf-8") as archivo:
        for certificado in certificados:
            archivo.write(certificado + "\n")

    print(f"Total de certificados pendientes: {len(certificados)}")
    if certificados:
        for certificado in certificados:
            print(certificado)
    else:
        print("No hay alumnos aprobados para certificar.")


def mostrar_reporte(alumnos, profesores):
    print("\n" + "=" * 70)
    print("REPORTE GENERAL SGA-DO")
    print("=" * 70)

    print("\n--- PROFESORES ACTIVOS ---")
    if not profesores:
        print("No hay profesores registrados.")
    for profesor in profesores.values():
        print(
            f"ID: {profesor.cedula} | Nombre: {profesor.nombre} | "
            f"Correo: {profesor.correo} | Especialidad: {profesor.especialidad} | "
            f"Materia: {profesor.materia}"
        )

    print("\n--- ALUMNOS REGISTRADOS ---")
    if not alumnos:
        print("No hay alumnos registrados.")
    for alumno in alumnos.values():
        notas = alumno.notas + [0] * (MAX_NOTAS - len(alumno.notas))
        if len(alumno.notas) < MAX_NOTAS:
            estado = "EN CURSO"
        elif alumno.esta_aprobado():
            estado = "APROBADO"
        else:
            estado = "REPROBADO"
        print(
            f"ID: {alumno.cedula} | Nombre: {alumno.nombre} | "
            f"Programa: {alumno.programa.nombre} | Notas: {notas} | "
            f"Promedio: {alumno.promedio():.2f} | Estatus: {estado}"
        )


def mostrar_menu():
    print("\n" + "=" * 50)
    print("SGA-DO: SISTEMA DIPLOMADOSONLINE")
    print("=" * 50)
    print("1. Registrar Alumno")
    print("2. Registrar Profesor")
    print("3. Registrar Notas a un Alumno")
    print("4. Deshacer Último Registro de Nota")
    print("5. Generar Cola de Certificados")
    print("6. Mostrar Reporte General")
    print("7. Salir")
    print("=" * 50)


def main():
    alumnos = cargar_alumnos()
    profesores = cargar_profesores()

    # Pila de operaciones de notas. Cada elemento contiene (cedula, nota).
    pila_notas = []

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            registrar_alumno(alumnos)
        elif opcion == "2":
            registrar_profesor(profesores)
        elif opcion == "3":
            registrar_nota(alumnos, pila_notas)
        elif opcion == "4":
            deshacer_ultima_nota(alumnos, pila_notas)
        elif opcion == "5":
            generar_cola_certificados(alumnos)
        elif opcion == "6":
            mostrar_reporte(alumnos, profesores)
        elif opcion == "7":
            guardar_alumnos(alumnos)
            guardar_profesores(profesores)
            print("\nCambios guardados. SGA-DO cerrado de forma segura.")
            break
        else:
            print("Opción no válida. Seleccione un número del 1 al 7.")


if __name__ == "__main__":
    main()
