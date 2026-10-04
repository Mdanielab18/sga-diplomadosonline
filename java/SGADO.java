import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.util.Stack;

public class SGADO {

    private static ArrayList<Alumno> alumnos = new ArrayList<>();
    private static ArrayList<Profesor> profesores = new ArrayList<>();

    // Cola FIFO para certificados
    private static Queue<Alumno> colaCertificados = new LinkedList<>();

    // Pila LIFO para deshacer la última nota
    private static Stack<String> pilaNotas = new Stack<>();

    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {

    ArchivoUtil.crearArchivos();

    alumnos = ArchivoUtil.cargarAlumnos();
    profesores = ArchivoUtil.cargarProfesores();

    int opcion;

        do {

            System.out.println("\n==================================================");
            System.out.println("SGA-DO: SISTEMA DIPLOMADOSONLINE");
            System.out.println("==================================================");
            System.out.println("1. Registrar Alumno");
            System.out.println("2. Registrar Profesor");
            System.out.println("3. Registrar Notas a un Alumno");
            System.out.println("4. Deshacer Último Registro de Nota");
            System.out.println("5. Generar Cola de Certificados");
            System.out.println("6. Mostrar Reporte General");
            System.out.println("7. Salir");
            System.out.println("==================================================");
            System.out.print("Seleccione una opción (1-7): ");

            opcion = scanner.nextInt();
            scanner.nextLine();

            switch (opcion) {

                case 1:
                    registrarAlumno();
                    break;

                case 2:
                    registrarProfesor();
                    break;

                case 3:
                    registrarNotas();
                    break;

                case 4:
                    deshacerUltimoRegistro();
                    break;

                case 5:
                    generarColaCertificados();
                    break;

                case 6:
                    mostrarReporteGeneral();
                    break;

                case 7:
                    System.out.println("\nSistema finalizado.");
                    break;

                default:
                    System.out.println("\nOpción inválida.");
            }

        } while (opcion != 7);

        scanner.close();
    }

    // ==================================================
    // 1. REGISTRAR ALUMNO
    // ==================================================

    private static void registrarAlumno() {

        System.out.println("\n--- REGISTRAR ALUMNO ---");

        System.out.print("Cédula: ");
        String cedula = scanner.nextLine();

        System.out.print("Nombre: ");
        String nombre = scanner.nextLine();

        System.out.print("Correo: ");
        String correo = scanner.nextLine();

        System.out.print("Programa (Curso/Diplomado/BootCamp): ");
        String programa = scanner.nextLine();

        Alumno alumno = new Alumno(
                cedula,
                nombre,
                correo,
                programa
        );

        alumnos.add(alumno);

        ArchivoUtil.guardarAlumnos(alumnos);

        System.out.println("\nAlumno registrado correctamente.");
    }

    // ==================================================
    // 2. REGISTRAR PROFESOR
    // ==================================================

    private static void registrarProfesor() {

        System.out.println("\n--- REGISTRAR PROFESOR ---");

        System.out.print("Cédula: ");
        String cedula = scanner.nextLine();

        System.out.print("Nombre: ");
        String nombre = scanner.nextLine();

        System.out.print("Correo: ");
        String correo = scanner.nextLine();

        System.out.print("Especialidad: ");
        String especialidad = scanner.nextLine();

        System.out.print("Materia: ");
        String materia = scanner.nextLine();

        Profesor profesor = new Profesor(
                cedula,
                nombre,
                correo,
                especialidad,
                materia
        );

        profesores.add(profesor);

        ArchivoUtil.guardarProfesores(profesores);

        System.out.println("\nProfesor registrado correctamente.");
    }

    // ==================================================
    // 3. REGISTRAR NOTAS A UN ALUMNO
    // ==================================================

    private static void registrarNotas() {

        System.out.println("\n--- REGISTRAR NOTAS A UN ALUMNO ---");

        System.out.print("Cédula del alumno: ");
        String cedula = scanner.nextLine();

        Alumno alumno = buscarAlumno(cedula);

        if (alumno == null) {
            System.out.println("\nAlumno no encontrado.");
            return;
        }

        if (alumno.getNotas().size() >= 3) {
            System.out.println("\nEl alumno ya tiene el máximo de 3 notas.");
            return;
        }

        System.out.print("Ingrese la nota: ");
        double nota = scanner.nextDouble();
        scanner.nextLine();

        if (nota < 0 || nota > 20) {
            System.out.println("\nLa nota debe estar entre 0 y 20.");
            return;
        }

        alumno.agregarNota(nota);

        /*
         * Se guarda la cédula en la pila.
         * Esto permite que la opción 4 pueda
         * deshacer automáticamente la última nota.
         */
        pilaNotas.push(cedula);

        ArchivoUtil.guardarAlumnos(alumnos);

        System.out.println("\nNota registrada correctamente.");
    }

    // ==================================================
    // 4. DESHACER ÚLTIMO REGISTRO DE NOTA
    // ==================================================

    private static void deshacerUltimoRegistro() {

        System.out.println("\n--- DESHACER ÚLTIMO REGISTRO DE NOTA ---");

        if (pilaNotas.isEmpty()) {
            System.out.println("No existen registros de notas para deshacer.");
            return;
        }

        /*
         * LIFO:
         * Se obtiene automáticamente la última
         * cédula almacenada en la pila.
         */
        String cedula = pilaNotas.pop();

        Alumno alumno = buscarAlumno(cedula);

        if (alumno != null) {

            alumno.eliminarUltimaNota();

            ArchivoUtil.guardarAlumnos(alumnos);

            System.out.println(
                    "Se eliminó la última nota registrada de: "
                    + alumno.getNombre()
            );

        } else {
            System.out.println("No se encontró el alumno.");
        }
    }

    // ==================================================
    // 5. GENERAR COLA DE CERTIFICADOS
    // ==================================================

    private static void generarColaCertificados() {

    System.out.println("\n--- GENERAR COLA DE CERTIFICADOS ---");

    // Recargar los alumnos desde el archivo
    alumnos = ArchivoUtil.cargarAlumnos();

    colaCertificados.clear();

    // Buscar alumnos aprobados
    for (Alumno alumno : alumnos) {

        if (alumno.getNotas().isEmpty()) {
            continue;
        }

        ProgramaAcademico programa = obtenerPrograma(alumno);

        if (programa != null &&
            programa.estudianteAprobado(alumno)) {

            colaCertificados.add(alumno);
        }
    }

    if (colaCertificados.isEmpty()) {

        ArchivoUtil.guardarCertificados(colaCertificados);

        System.out.println(
                "No hay alumnos aprobados para generar certificados."
        );

        return;
    }

    System.out.println("\nCola de certificados:");

    for (Alumno alumno : colaCertificados) {

        System.out.println(
                "Cédula: " + alumno.getCedula()
                + " | Nombre: " + alumno.getNombre()
                + " | Programa: " + alumno.getPrograma()
        );
    }

    ArchivoUtil.guardarCertificados(colaCertificados);

System.out.println("\nCertificados generados correctamente.");
System.out.println("Total de certificados: " + colaCertificados.size());

}

    // ==================================================
    // 6. MOSTRAR REPORTE GENERAL
    // ==================================================

    private static void mostrarReporteGeneral() {

        System.out.println("\n==================================================");
        System.out.println("              REPORTE GENERAL");
        System.out.println("==================================================");

        // ---------- PROFESORES ----------

        System.out.println("\n--- PROFESORES REGISTRADOS ---");

        if (profesores.isEmpty()) {

            System.out.println("No hay profesores registrados.");

        } else {

            for (Profesor profesor : profesores) {

                System.out.println(
                        "Cédula: " + profesor.getCedula()
                        + " | Nombre: " + profesor.getNombre()
                        + " | Correo: " + profesor.getCorreo()
                        + " | Especialidad: " + profesor.getEspecialidad()
                        + " | Materia: " + profesor.getMateria()
                );
            }
        }

        // ---------- ALUMNOS ----------

        System.out.println("\n--- ALUMNOS REGISTRADOS ---");

        if (alumnos.isEmpty()) {

            System.out.println("No hay alumnos registrados.");

        } else {

            for (Alumno alumno : alumnos) {

                String estado = obtenerEstadoAlumno(alumno);

                System.out.println(
                        "Cédula: " + alumno.getCedula()
                        + " | Nombre: " + alumno.getNombre()
                        + " | Programa: " + alumno.getPrograma()
                        + " | Notas: " + alumno.getNotas()
                        + " | Promedio: "
                        + String.format("%.2f", alumno.calcularPromedio())
                        + " | Estado: " + estado
                );
            }
        }
    }

    // ==================================================
    // BUSCAR ALUMNO
    // ==================================================

    private static Alumno buscarAlumno(String cedula) {

        for (Alumno alumno : alumnos) {

            if (alumno.getCedula().equals(cedula)) {
                return alumno;
            }
        }

        return null;
    }

    // ==================================================
    // OBTENER PROGRAMA ACADÉMICO
    // ==================================================

    private static ProgramaAcademico obtenerPrograma(Alumno alumno) {

        String programa = alumno.getPrograma().toLowerCase();

        switch (programa) {

            case "curso":
                return new Curso();

            case "diplomado":
                return new Diplomado();

            case "bootcamp":
            case "boot camp":
                return new BootCamp();

            default:
                return null;
        }
    }

    // ==================================================
    // OBTENER ESTADO DEL ALUMNO
    // ==================================================

    private static String obtenerEstadoAlumno(Alumno alumno) {

        if (alumno.getNotas().isEmpty()) {
            return "SIN NOTAS";
        }

        ProgramaAcademico programa = obtenerPrograma(alumno);

        if (programa == null) {
            return "PROGRAMA NO VÁLIDO";
        }

        if (programa.estudianteAprobado(alumno)) {
            return "APROBADO";
        }

        return "REPROBADO";
    }
}