public class Diplomado extends ProgramaAcademico {

    public Diplomado() {
        super("Diplomado");
    }

    @Override
    public boolean estudianteAprobado(Alumno alumno) {
        return alumno.calcularPromedio() >= 14;
    }
}