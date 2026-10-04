import java.util.ArrayList;

public class Alumno extends Persona {
    private String programa;
    private ArrayList<Double> notas;

    public Alumno(String cedula, String nombre, String correo, String programa) {
        super(cedula, nombre, correo);
        this.programa = programa;
        this.notas = new ArrayList<>();
    }

    public String getPrograma() {
        return programa;
    }

    public ArrayList<Double> getNotas() {
        return notas;
    }

    public void agregarNota(double nota) {
        if (notas.size() < 3) {
            notas.add(nota);
        }
    }

    public void eliminarUltimaNota() {
        if (!notas.isEmpty()) {
            notas.remove(notas.size() - 1);
        }
    }

    public double calcularPromedio() {
        if (notas.isEmpty()) {
            return 0;
        }

        double suma = 0;

        for (double nota : notas) {
            suma += nota;
        }

        return suma / notas.size();
    }
}