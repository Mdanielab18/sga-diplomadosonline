import java.io.*;
import java.util.ArrayList;
import java.util.Queue;

public class ArchivoUtil {

    private static final String ARCHIVO_ALUMNOS = "alumnos.txt";
    private static final String ARCHIVO_PROFESORES = "profesores.txt";
    private static final String ARCHIVO_CERTIFICADOS = "certificados_pendientes.txt";

    // ==================================================
    // CREAR ARCHIVOS SI NO EXISTEN
    // ==================================================

    public static void crearArchivos() {

        try {
            new File(ARCHIVO_ALUMNOS).createNewFile();
            new File(ARCHIVO_PROFESORES).createNewFile();
            new File(ARCHIVO_CERTIFICADOS).createNewFile();

        } catch (IOException e) {
            System.out.println("Error al crear los archivos.");
        }
    }

    // ==================================================
    // GUARDAR ALUMNOS
    // ==================================================

    public static void guardarAlumnos(ArrayList<Alumno> alumnos) {

        try (BufferedWriter escritor =
                     new BufferedWriter(new FileWriter(ARCHIVO_ALUMNOS))) {

            for (Alumno alumno : alumnos) {

                StringBuilder linea = new StringBuilder();

                linea.append(alumno.getCedula()).append(",");
                linea.append(alumno.getNombre()).append(",");
                linea.append(alumno.getCorreo()).append(",");
                linea.append(alumno.getPrograma());

                for (double nota : alumno.getNotas()) {
                    linea.append(",").append(nota);
                }

                escritor.write(linea.toString());
                escritor.newLine();
            }

        } catch (IOException e) {
            System.out.println("Error al guardar alumnos.");
        }
    }

    // ==================================================
    // CARGAR ALUMNOS
    // ==================================================

    public static ArrayList<Alumno> cargarAlumnos() {

        ArrayList<Alumno> alumnos = new ArrayList<>();

        File archivo = new File(ARCHIVO_ALUMNOS);

        if (!archivo.exists()) {
            return alumnos;
        }

        try (BufferedReader lector =
                     new BufferedReader(new FileReader(archivo))) {

            String linea;

            while ((linea = lector.readLine()) != null) {

                if (linea.trim().isEmpty()) {
                    continue;
                }

                String[] datos = linea.split(",");

                if (datos.length < 4) {
                    continue;
                }

                String cedula = datos[0];
                String nombre = datos[1];
                String correo = datos[2];
                String programa = datos[3];

                Alumno alumno =
                        new Alumno(cedula, nombre, correo, programa);

                // Cargar las notas existentes
                for (int i = 4; i < datos.length && i < 7; i++) {

                    try {
                        double nota = Double.parseDouble(datos[i]);
                        alumno.agregarNota(nota);

                    } catch (NumberFormatException e) {
                        System.out.println(
                                "Nota inválida para el alumno "
                                + cedula
                        );
                    }
                }

                alumnos.add(alumno);
            }

        } catch (IOException e) {
            System.out.println("Error al cargar alumnos.");
        }

        return alumnos;
    }

    // ==================================================
    // GUARDAR PROFESORES
    // ==================================================

    public static void guardarProfesores(ArrayList<Profesor> profesores) {

        try (BufferedWriter escritor =
                     new BufferedWriter(new FileWriter(ARCHIVO_PROFESORES))) {

            for (Profesor profesor : profesores) {

                escritor.write(
                        profesor.getCedula() + ","
                        + profesor.getNombre() + ","
                        + profesor.getCorreo() + ","
                        + profesor.getEspecialidad() + ","
                        + profesor.getMateria()
                );

                escritor.newLine();
            }

        } catch (IOException e) {
            System.out.println("Error al guardar profesores.");
        }
    }

    // ==================================================
    // CARGAR PROFESORES
    // ==================================================

    public static ArrayList<Profesor> cargarProfesores() {

        ArrayList<Profesor> profesores = new ArrayList<>();

        File archivo = new File(ARCHIVO_PROFESORES);

        if (!archivo.exists()) {
            return profesores;
        }

        try (BufferedReader lector =
                     new BufferedReader(new FileReader(archivo))) {

            String linea;

            while ((linea = lector.readLine()) != null) {

                if (linea.trim().isEmpty()) {
                    continue;
                }

                String[] datos = linea.split(",");

                if (datos.length < 5) {
                    continue;
                }

                Profesor profesor = new Profesor(
                        datos[0],
                        datos[1],
                        datos[2],
                        datos[3],
                        datos[4]
                );

                profesores.add(profesor);
            }

        } catch (IOException e) {
            System.out.println("Error al cargar profesores.");
        }

        return profesores;
    }

    // ==================================================
    // GUARDAR CERTIFICADOS
    // ==================================================

    public static void guardarCertificados(Queue<Alumno> cola) {

        try (BufferedWriter escritor =
                     new BufferedWriter(new FileWriter(ARCHIVO_CERTIFICADOS))) {

            for (Alumno alumno : cola) {

                escritor.write(
                        alumno.getCedula() + ","
                        + alumno.getNombre() + ","
                        + alumno.getCorreo() + ","
                        + alumno.getPrograma()
                );

                escritor.newLine();
            }

        } catch (IOException e) {
            System.out.println("Error al guardar certificados.");
        }
    }
}