public class Curso extends ProgramaAcademico {

    public Curso() {
        super("Curso");
    }

    @Override
    public boolean estudianteAprobado(Alumno alumno) {
        return alumno.calcularPromedio() >= 10;
    }
}
